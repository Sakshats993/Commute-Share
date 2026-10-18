import test from "node:test";
import assert from "node:assert/strict";

import { normalizeIndianMobileNumber } from "./phone.js";

test("accepts a ten-digit Indian mobile number", () => {
    assert.equal(normalizeIndianMobileNumber("9876543210"), "9876543210");
});

test("normalizes a number with the +91 country code and formatting", () => {
    assert.equal(normalizeIndianMobileNumber("+91 98765-43210"), "9876543210");
});

test("normalizes an unformatted 91 country prefix", () => {
    assert.equal(normalizeIndianMobileNumber("919876543210"), "9876543210");
});

test("rejects invalid, incomplete, and non-Indian mobile numbers", () => {
    for (const value of ["", "1234567890", "+1 9876543210", "+91 1234567890", "98765"]) {
        assert.equal(normalizeIndianMobileNumber(value), null);
    }
});
