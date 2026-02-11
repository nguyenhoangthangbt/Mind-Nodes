"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import type { TokenResponse } from "@/types";
import { useAuth } from "@/stores/auth";

export default function VerifyPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { fetchUser } = useAuth();

  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const token = searchParams.get("token");

    if (!token) {
      setStatus("error");
      setErrorMessage("No verification token found. Please request a new magic link.");
      return;
    }

    const verify = async () => {
      try {
        const tokens = await api.post<TokenResponse>("/api/v1/auth/magic-link/verify", {
          token,
        });

        api.setToken(tokens.access_token);
        localStorage.setItem("refresh_token", tokens.refresh_token);

        await fetchUser();

        setStatus("success");

        // Brief delay so the user sees the success state before redirect
        setTimeout(() => {
          router.push("/dashboard");
        }, 1000);
      } catch (err: any) {
        setStatus("error");
        setErrorMessage(
          err.message || "Verification failed. The link may have expired or already been used."
        );
      }
    };

    verify();
  }, [searchParams, router, fetchUser]);

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-sm text-center">
        {status === "loading" && (
          <>
            <div className="mx-auto mb-6 h-12 w-12 animate-spin rounded-full border-4 border-gray-200 border-t-primary-600" />
            <h1 className="text-xl font-semibold text-gray-900">Verifying your link...</h1>
            <p className="mt-2 text-sm text-gray-500">
              Please wait while we verify your magic link.
            </p>
          </>
        )}

        {status === "success" && (
          <>
            <div className="mx-auto mb-6 flex h-14 w-14 items-center justify-center rounded-full bg-green-100">
              <svg
                className="h-7 w-7 text-green-600"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="m4.5 12.75 6 6 9-13.5"
                />
              </svg>
            </div>
            <h1 className="text-xl font-semibold text-gray-900">Verified!</h1>
            <p className="mt-2 text-sm text-gray-500">
              Redirecting you to the dashboard...
            </p>
          </>
        )}

        {status === "error" && (
          <>
            <div className="mx-auto mb-6 flex h-14 w-14 items-center justify-center rounded-full bg-red-100">
              <svg
                className="h-7 w-7 text-red-600"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M6 18 18 6M6 6l12 12"
                />
              </svg>
            </div>
            <h1 className="text-xl font-semibold text-gray-900">Verification Failed</h1>
            <p className="mt-2 text-sm text-gray-500">{errorMessage}</p>
            <div className="mt-6">
              <Link
                href="/auth/login"
                className="inline-block rounded-md bg-primary-600 px-6 py-2 text-sm font-semibold text-white hover:bg-primary-700"
              >
                Back to Login
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
