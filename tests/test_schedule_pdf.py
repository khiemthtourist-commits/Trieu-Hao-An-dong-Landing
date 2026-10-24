import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import sync_schedule as sync

class PDFTests(unittest.TestCase):
    def test_whole_words_avoid_wrong_hainan_detail(self):
        self.assertIsNone(sync.match_slug('NAM KINH - THƯỢNG HẢI','TQ241026NK'))
        self.assertIsNone(sync.match_slug('TẾ NAM - THANH ĐẢO','TQ241026TD'))
        self.assertEqual(sync.match_slug('ĐẢO HẢI NAM','TQ241026HN'),'trungquoc-hai-nam')

    def test_each_row_keeps_own_pdf_even_same_code_or_route(self):
        common=dict(ten='ĐÀI LOAN',vung='ĐÀI LOAN',dip='',maLich='same',thoiLuong='5N4D',ngayDi='24/10/2026',ngayVe='28/10/2026',bayDi='BR',bayVe='',soCho=10,conCho=5,giaGoc='',giaSale='')
        rows=[dict(common,id=1,pdf='/Uploads/EVA.pdf'),dict(common,id=2,pdf='/Uploads/VJ.pdf',bayDi='VJ',ngayDi='25/10/2026'),dict(common,id=3,pdf=None)]
        with patch.object(sync,'extract_row',side_effect=lambda x:x),patch.object(sync,'match_slug',return_value='local-old-tour'):
            result=sync.build_schedule_data(rows)
        byid={r['id']:r for r in result}
        self.assertEqual(byid[1]['pdfExternal'],sync.BASE+'/Uploads/EVA.pdf')
        self.assertEqual(byid[2]['pdfExternal'],sync.BASE+'/Uploads/VJ.pdf')
        self.assertIsNone(byid[3]['pdfExternal'])

    def test_reject_untrusted_pdf_host(self):
        self.assertIsNone(sync.source_pdf_url('https://other.example/brochure.pdf'))
        self.assertIsNone(sync.source_pdf_url('javascript:alert(1)'))
        self.assertEqual(sync.source_pdf_url('/Uploads/program.pdf'),sync.BASE+'/Uploads/program.pdf')

if __name__=='__main__':unittest.main()
