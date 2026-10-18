import test from "node:test";
import assert from "node:assert/strict";

import { passwordsMatch } from "./passwordConfirmation.js";

test("accepts matching password confirmation", () => {
    assert.equal(passwordsMatch("CorrectHorse9!", "CorrectHorse9!"), true);
});

test("rejects a different password confirmation", () => {
    assert.equal(passwordsMatch("CorrectHorse9!", "CorrectHorse9"), false);
});

