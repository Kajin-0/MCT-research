import json
import unittest
from build_transport import PRIVATE
from envelope import wave_file_payload,density_file_payload,collected_writer_scratch,mixing_history,require_complete,report,Refusal


class EnvelopeTest(unittest.TestCase):
    def test_datasets_include_Miller_indices(self):
        self.assertEqual(wave_file_payload(17,2,48),16*17*2*48+12*17)
        self.assertEqual(density_file_payload(17,4),16*17*4+12*17)
    def test_scratch_phase_max_not_sum_and_density_label_not_wave_count(self):
        a=collected_writer_scratch(17,12,100,2,10,25,8)
        self.assertEqual(a['wave_selected_peak_bytes'],20*12+4*8+8*100+4*17)
        self.assertEqual(a['density_selected_root_peak_bytes'],16*(25+10))
        self.assertFalse(a['native_merge_MPI_HDF5_included'])
    def test_mix_buffer_storage_location_and_max_record(self):
        ram=mixing_history(17,4,8,0);disk=mixing_history(17,4,8,1)
        self.assertEqual(ram['max_record_index'],18)
        self.assertEqual(ram['history_RAM_payload_bytes'],disk['active_history_disk_logical_bytes'])
        self.assertEqual(ram['active_history_disk_logical_bytes'],0);self.assertEqual(disk['history_RAM_payload_bytes'],0)
        self.assertEqual(ram['kept_history_disk_logical_upper_bytes'],disk['kept_history_disk_logical_upper_bytes'])
        self.assertGreater(ram['kept_history_disk_logical_upper_bytes'],0)
        self.assertEqual(ram['RAM_close_keep_extra_vector_bytes'],ram['record_bytes'])
        with self.assertRaises(Refusal):mixing_history(17,4,26,1)
    def test_checked_int64_and_UNKNOWN_never_zero(self):
        with self.assertRaises(Refusal):wave_file_payload(1<<62,2,48)
        with self.assertRaisesRegex(Refusal,'UNKNOWN'):require_complete({})
        r=report();self.assertFalse(r['whole_disk_envelope_certified']);self.assertFalse(r['whole_RSS_envelope_certified'])


if __name__=='__main__':
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(EnvelopeTest))
    (PRIVATE/'envelope_tests.json').write_text(json.dumps({'passed':r.wasSuccessful(),'methods':r.testsRun,'selected_envelope':report()},indent=2)+'\n')
    raise SystemExit(0 if r.wasSuccessful() else 1)
