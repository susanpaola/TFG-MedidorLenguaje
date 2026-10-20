import unittest

from negocio.services.bias_analysis_service import analyze_text


class BiasAnalysisServiceTests(unittest.TestCase):
    def test_detects_age_stereotype_only_with_full_context(self):
        findings = analyze_text("Las personas mayores no entienden la tecnología.")

        self.assertEqual(findings[0]["rule_id"], "edad-tecnologia-001")

    def test_does_not_flag_technology_without_negative_stereotype(self):
        findings = analyze_text("Las personas mayores participan en un curso de tecnología.")

        self.assertEqual(findings, [])

    def test_marks_generic_masculine_as_a_low_severity_suggestion(self):
        findings = analyze_text("Los alumnos entregarán el trabajo el viernes.")

        self.assertEqual(findings[0]["analysis_type"], "sugerencia_lenguaje_inclusivo")
        self.assertEqual(findings[0]["severity"], "baja")


if __name__ == "__main__":
    unittest.main()
