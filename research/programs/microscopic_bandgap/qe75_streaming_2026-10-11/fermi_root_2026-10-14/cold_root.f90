! GPL-2.0-or-later. PRIVATE bounded 48-band one-pool cold root qualification.
! wgauss/gweights/EXX are unchanged. No squared-charge minimization.
MODULE r07_cold_root
 USE kinds,ONLY:DP
 USE,INTRINSIC::ieee_arithmetic,ONLY:ieee_is_finite
 IMPLICIT NONE
 REAL(DP),SAVE::last_certificate(10)=0._DP
 REAL(DP),PARAMETER::charge_tol=1.e-10_DP, fpad=1.e-11_DP,dpad=1.e-8_DP,mfloor=1.e-6_DP
 INTEGER,PARAMETER::max_nodes=8192,max_bisect=256
CONTAINS
 SUBROUTINE strict_root(et,nb,nk,ne,wk,sigma,is,isk,mu,code)
  INTEGER,INTENT(IN)::nb,nk,is,isk(nk)
  REAL(DP),INTENT(IN)::et(nb,nk),ne,wk(nk),sigma
  REAL(DP),INTENT(OUT)::mu
  INTEGER,INTENT(OUT)::code
  REAL(DP),EXTERNAL::sumkg
  REAL(DP)::energy(nb*nk),weight(nb*nk),e,w,total,global_lo,global_hi,lo,hi,mid,flo,fhi,fm
  REAL(DP)::radius,rlo,rhi,dl,du,fl,fu,a,b,fa,fb,ls(max_nodes),us(max_nodes)
  INTEGER::i,j,k,n,l,it,visited,stack,level
  code=1;mu=0._DP;last_certificate=0._DP
  IF(nb/=48.OR.nk/=3.OR.is/=0.OR.ne/=36._DP.OR.sigma/=.001_DP) RETURN
  IF(ANY(wk/=[.125_DP,.5_DP,.375_DP])) RETURN
  IF(.NOT.ALL(ieee_is_finite(et))) RETURN
  IF(MAXVAL(ABS(et))>100._DP) RETURN ! finite qualification envelope, no overflow oracle
  DO k=1,nk
   IF(ANY(et(2:nb,k)<et(1:nb-1,k))) RETURN
  ENDDO
  n=0
  DO k=1,nk
   DO j=1,nb
    n=n+1;energy(n)=et(j,k);weight(n)=wk(k)
   ENDDO
  ENDDO
  DO i=2,n
   e=energy(i);w=weight(i);j=i-1
   DO WHILE(j>=1)
    IF(energy(j)<=e) EXIT
    energy(j+1)=energy(j);weight(j+1)=weight(j);j=j-1
   ENDDO
   energy(j+1)=e;weight(j+1)=w
  ENDDO
  ! Analytical exclusion: fmax<1.1, f(-10)<1e-49; f(x)>=1 for x>=sqrt(2).
  total=0._DP;l=0
  DO i=1,n
   total=total+weight(i)
   IF(l==0.AND.total>=ne/1.1_DP) THEN
    global_lo=energy(i)-10._DP*sigma;l=1
   ENDIF
   IF(total>=ne) THEN
    global_hi=energy(i)+SQRT(2._DP)*sigma;EXIT
   ENDIF
  ENDDO
  IF(l/=1.OR.global_lo>=global_hi) RETURN
  lo=global_lo;hi=global_hi
  flo=count(lo)-ne;fhi=count(hi)-ne
  IF(.NOT.ieee_is_finite(flo).OR..NOT.ieee_is_finite(fhi)) RETURN
  IF(flo>=-fpad.OR.fhi<=fpad) THEN
   code=2;RETURN
  ENDIF
  DO it=1,max_bisect
   mid=lo+(hi-lo)/2._DP
   IF(mid==lo.OR.mid==hi) THEN
    code=3;RETURN
   ENDIF
   fm=count(mid)-ne
   IF(.NOT.ieee_is_finite(fm)) RETURN
   IF(ABS(fm)<=charge_tol) EXIT
   IF(fm<0._DP) THEN
    lo=mid
   ELSE
    hi=mid
   ENDIF
  ENDDO
  IF(it>max_bisect) THEN
   code=3;RETURN
  ENDIF
  mu=mid
  ! A strong increasing neighborhood is required; never accept a flat plateau.
  radius=sigma/64._DP
  DO level=1,48
   rlo=MAX(global_lo,mu-radius);rhi=MIN(global_hi,mu+radius)
   CALL bounds(rlo,rhi,fl,fu,dl,du)
   fa=count(rlo)-ne;fb=count(rhi)-ne
   IF(dl>mfloor.AND.fa< -fpad.AND.fb>fpad) EXIT
   radius=radius/2._DP
  ENDDO
  IF(level>48) THEN
   code=4;RETURN
  ENDIF
  ! Prove no additional root in the rest of the complete admissible domain.
  stack=2;ls(1)=global_lo;us(1)=rlo;ls(2)=rhi;us(2)=global_hi;visited=0
  DO WHILE(stack>0)
   a=ls(stack);b=us(stack);stack=stack-1
   IF(b<=a) CYCLE
   visited=visited+1
   IF(visited>max_nodes-4) THEN
    code=5;RETURN
   ENDIF
   CALL bounds(a,b,fl,fu,dl,du)
   IF(fl>ne.OR.fu<ne) CYCLE
   fa=count(a)-ne;fb=count(b)-ne
   IF(dl>0._DP.OR.du<0._DP) THEN
    IF(MIN(fa,fb)>fpad.OR.MAX(fa,fb)<-fpad) CYCLE
    IF(MIN(fa,fb)<-fpad.AND.MAX(fa,fb)>fpad) THEN
     code=6;RETURN ! competing actual zero, not a permission to choose arbitrarily
    ENDIF
   ENDIF
   mid=a+(b-a)/2._DP
   IF(mid==a.OR.mid==b.OR.stack+2>max_nodes) THEN
    code=5;RETURN
   ENDIF
   stack=stack+1;ls(stack)=a;us(stack)=mid
   stack=stack+1;ls(stack)=mid;us(stack)=b
  ENDDO
  CALL bounds(rlo,rhi,fl,fu,dl,du)
  fm=count(mu)-ne
  IF(ABS(fm)>charge_tol.OR.dl<=mfloor) THEN
   code=7;RETURN
  ENDIF
  last_certificate=[global_lo,global_hi,rlo,rhi,dl,du,fm,REAL(it,DP),REAL(visited,DP),fpad]
  code=0
 CONTAINS
  FUNCTION count(x) RESULT(value)
   REAL(DP),INTENT(IN)::x
   REAL(DP)::value
   value=sumkg(et,nb,nk,wk,sigma,-1,x,is,isk)
  END FUNCTION
  SUBROUTINE bounds(a,b,fl,fu,dl,du)
   REAL(DP),INTENT(IN)::a,b
   REAL(DP),INTENT(OUT)::fl,fu,dl,du
   REAL(DP),EXTERNAL::wgauss,w0gauss
   REAL(DP)::x1,x2,c1,c2,f1,f2,flow,fup,dlo,dup,d
   INTEGER::ii,kk
   c1=(3._DP-SQRT(5._DP))/(2._DP*SQRT(2._DP))
   c2=(3._DP+SQRT(5._DP))/(2._DP*SQRT(2._DP))
   fl=0._DP;fu=0._DP;dl=0._DP;du=0._DP
   DO kk=1,nk
    DO ii=1,nb
     x1=(a-et(ii,kk))/sigma;x2=(b-et(ii,kk))/sigma
     f1=wgauss(x1,-1);f2=wgauss(x2,-1)
     flow=MIN(f1,f2);fup=MAX(f1,f2)
     IF(x1<=SQRT(2._DP).AND.x2>=SQRT(2._DP)) fup=MAX(fup,wgauss(SQRT(2._DP),-1))
     fl=fl+wk(kk)*flow;fu=fu+wk(kk)*fup
     dlo=MIN(w0gauss(x1,-1),w0gauss(x2,-1));dup=MAX(w0gauss(x1,-1),w0gauss(x2,-1))
     IF(x1<=c1.AND.x2>=c1) THEN
      d=w0gauss(c1,-1);dlo=MIN(dlo,d);dup=MAX(dup,d)
     ENDIF
     IF(x1<=c2.AND.x2>=c2) THEN
      d=w0gauss(c2,-1);dlo=MIN(dlo,d);dup=MAX(dup,d)
     ENDIF
     dl=dl+wk(kk)*dlo/sigma;du=du+wk(kk)*dup/sigma
    ENDDO
   ENDDO
   fl=fl-fpad;fu=fu+fpad;dl=dl-dpad;du=du+dpad
  END SUBROUTINE
 END SUBROUTINE
END MODULE
