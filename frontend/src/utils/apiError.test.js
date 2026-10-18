import assert from "node:assert/strict";
import test from "node:test";

import { getApiErrorMessage } from "./apiError.js";

test("formats FastAPI validation errors", () => {
    const error = {
        response: {
            data: {
                detail: [
                    { msg: "Pickup is required" },
                    { msg: "Destination is required" },
                ],
            },
        },
    };

    assert.equal(
        getApiErrorMessage(error, "Fallback"),
        "Pickup is required, Destination is required"
    );
});

test("uses a server-provided message when present", () => {
    assert.equal(
        getApiErrorMessage(
            { response: { data: { detail: "Access denied" } } },
            "Fallback"
        ),
        "Access denied"
    );
});

test("falls back when the response has no usable detail", () => {
    assert.equal(
        getApiErrorMessage(new Error("network failure"), "Please retry"),
        "Please retry"
    );
});
