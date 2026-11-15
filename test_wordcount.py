import shutil
import subprocess
import tempfile#создание временных папок для тестов
import unittest
from pathlib import Path

SOURCE = Path(__file__).with_name('main.cpp')#прописываем путь к с++ файлу


class WordCountTestCase(unittest.TestCase):
    @classmethod#создаем папку с временными файлами
    def setUpClass(cls):
        cls.workdir = tempfile.TemporaryDirectory(prefix='wordcount_tests_')
        cls.root = Path(cls.workdir.name)
        cls.binary = cls.root / 'wordcount'
        compiler = shutil.which('g++') or shutil.which('clang++')
        if compiler is None:
            raise RuntimeError('Need c++ compiler')
        subprocess.run([compiler, '-std=c++17', '-O0', '-o', str(cls.binary), str(SOURCE)], check=True, capture_output=True, text=True)

    @classmethod#отчистка 
    def tearDownClass(cls):
        cls.workdir.cleanup()

    def run_program(self, content=b'', *flags, filename='sample.txt'):
        file = self.root / filename
        file.write_bytes(content if isinstance(content, bytes) else content.encode('utf-8'))
        result = subprocess.run([str(self.binary), *flags, filename], cwd=self.root, capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        return result.stdout

    def test_01_simple_text(self):
        result = self.run_program('Hello world')
        self.assertEqual(result, '1 2 11 sample.txt\n')

    def test_02_text_with_newline(self):
        result = self.run_program('Hello world\n')
        self.assertEqual(result, '1 2 12 sample.txt\n')

    def test_03_empty_file(self):
        result = self.run_program('')
        self.assertEqual(result, '0 0 0 sample.txt\n')

    def test_04_one_letter(self):
        result = self.run_program('A')
        self.assertEqual(result, '1 1 1 sample.txt\n')

    def test_05_one_newline(self):
        result = self.run_program('\n')
        self.assertEqual(result, '1 0 1 sample.txt\n')

    def test_06_two_empty_lines(self):
        result = self.run_program('\n\n')
        self.assertEqual(result, '2 0 2 sample.txt\n')

    def test_07_two_lines_without_final_newline(self):
        result = self.run_program('abc\ndef')
        self.assertEqual(result, '2 2 7 sample.txt\n')

    def test_08_two_lines_with_final_newline(self):
        result = self.run_program('abc\ndef\n')
        self.assertEqual(result, '2 2 8 sample.txt\n')

    def test_09_spaces(self):
        result = self.run_program('  one   two  ')
        self.assertEqual(result, '1 2 13 sample.txt\n')

    def test_10_only_spaces(self):
        result = self.run_program('   ')
        self.assertEqual(result, '1 0 3 sample.txt\n')

    def test_11_tabs(self):
        result = self.run_program('one\ttwo')
        self.assertEqual(result, '1 2 7 sample.txt\n')

    def test_12_crlf(self):
        result = self.run_program(b'one\r\ntwo\r\n')
        self.assertEqual(result, '2 2 10 sample.txt\n')

    def test_13_punctuation(self):
        result = self.run_program('hi, world!')
        self.assertEqual(result, '1 2 10 sample.txt\n')

    def test_14_digits(self):
        result = self.run_program('123 45')
        self.assertEqual(result, '1 2 6 sample.txt\n')

    def test_15_long_lines_option(self):
        result = self.run_program('a\nb\n', '--lines')
        self.assertEqual(result, '2 sample.txt\n')

    def test_16_long_words_option(self):
        result = self.run_program('a bb ccc', '--words')
        self.assertEqual(result, '3 sample.txt\n')

    def test_17_long_bytes_option(self):
        result = self.run_program('abc def', '--bytes')
        self.assertEqual(result, '7 sample.txt\n')

    def test_18_long_alnum_option(self):
        result = self.run_program('ab! 12? C', '--alnum')
        self.assertEqual(result, '5 sample.txt\n')

    def test_19_short_lines_option(self):
        result = self.run_program('one\ntwo', '-l')
        self.assertEqual(result, '2 sample.txt\n')

    def test_20_short_words_option(self):
        result = self.run_program('one two', '-w')
        self.assertEqual(result, '2 sample.txt\n')

    def test_21_short_bytes_option(self):
        result = self.run_program('one two', '-c')
        self.assertEqual(result, '7 sample.txt\n')

    def test_22_short_alnum_option(self):
        result = self.run_program('a?2', '-a')
        self.assertEqual(result, '2 sample.txt\n')

    def test_23_combined_short_options(self):
        result = self.run_program('hi 42!', '-lwa')
        self.assertEqual(result, '1 2 4 sample.txt\n')

    def test_24_all_options(self):
        result = self.run_program('hi 42!', '--lines', '--words', '--bytes', '--alnum')
        self.assertEqual(result, '1 2 4 6 sample.txt\n')

    def test_25_filename_with_spaces(self):
        result = self.run_program('hello', '--words', filename='my sample.txt')
        self.assertEqual(result, '1 my sample.txt\n')

    def test_26_unicode_bytes(self):
        result = self.run_program('Привет', '--bytes')
        self.assertEqual(result, '12 sample.txt\n')

    def test_27_unicode_ascii_alnum(self):
        result = self.run_program('привет A2!', '--alnum')
        self.assertEqual(result, '2 sample.txt\n')

    def test_28_no_arguments(self):
        result = subprocess.run([str(self.binary)], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.stdout, 'No file.')

    def test_29_two_files(self):
        (self.root / 'first.txt').write_text('a b', encoding='utf-8')
        (self.root / 'second.txt').write_text('xy', encoding='utf-8')
        result = subprocess.run([str(self.binary), '--words', 'first.txt', 'second.txt'], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.stdout, '2 first.txt\n1 second.txt\n')

    def test_30_only_flag_no_filename(self):
        #ожидаем диагностическое сообщение, если нет имени файла
        result = subprocess.run([str(self.binary), '--words'], cwd=self.root, capture_output=True, text=True)
        self.assertIn('No file', result.stdout + result.stderr)

    def test_31_missing_file(self):
        #ожидаем ошибку открытия файла, а не 0 0 0
        result = subprocess.run([str(self.binary), 'missing.txt'], cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(result.stdout, '0 0 0 missing.txt\n')
        self.assertTrue(result.returncode != 0 or result.stderr or 'error' in result.stdout.lower() or 'not found' in result.stdout.lower())


if __name__ == '__main__':
    unittest.main(verbosity=2)
