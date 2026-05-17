import unittest

import grok_credits


SAMPLE_GRPC_WEB_HEX = (
    "000000003c"
    "0a3a0d8988083e12001a0022060880dacfcf062a06088097f3d006"
    "32090a0508ea0f1004120032090a0508ea0f1003120032090a0508ea0f10021200"
    "800000000f677270632d7374617475733a300d0a"
)


class GrokCreditsParserTest(unittest.TestCase):
    def test_decode_and_parse_sample_meter(self):
        payload = grok_credits._decode_grpc_web_response(bytes.fromhex(SAMPLE_GRPC_WEB_HEX), {})
        report = grok_credits.parse_get_grok_credits_config_response(payload)

        self.assertEqual(report["plan"], "SuperGrok Heavy")
        self.assertAlmostEqual(report["credit_usage_percent"], 0.13333334028720856)
        self.assertEqual(report["credit_usage_display"], "<1% used")
        self.assertEqual(report["billing_period_start"]["iso_utc"], "2026-05-01T00:00:00+00:00")
        self.assertEqual(report["billing_period_end"]["iso_utc"], "2026-06-01T00:00:00+00:00")
        self.assertFalse(report["on_demand_enabled"])
        self.assertEqual([h["month"] for h in report["history"]], [4, 3, 2])

    def test_refuses_non_grok_endpoint_by_default(self):
        token = "x" * 64
        with self.assertRaises(grok_credits.GrokCreditsError) as cm:
            grok_credits.call_get_grok_credits_config(
                "https://example.com/grok_api_v2.GrokBuildBilling/GetGrokCreditsConfig",
                token,
                0.01,
            )

        message = str(cm.exception)
        self.assertIn("non-grok.com endpoint", message)
        self.assertNotIn(token, message)

    def test_error_redaction(self):
        redact = getattr(grok_credits, "_redact_sensitive")
        redacted = redact("Authorization: Bearer " + ("a" * 64))
        self.assertEqual(redacted, "Authorization: Bearer [REDACTED]")


if __name__ == "__main__":
    unittest.main()
