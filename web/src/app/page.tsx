import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-4">
      <div className="max-w-2xl text-center">
        <h1 className="text-5xl font-bold tracking-tight text-gray-900">
          Lead<span className="text-primary-600">Local</span>
        </h1>
        <p className="mt-4 text-xl text-gray-600">
          Discover local businesses. Build your pipeline. Close more deals.
        </p>
        <p className="mt-2 text-gray-500">
          Search Google Places, save leads, add notes, set reminders, and track
          your sales pipeline — all in one tool built for agencies and freelancers.
        </p>
        <div className="mt-8 flex justify-center gap-4">
          <Link
            href="/auth/signup"
            className="rounded-lg bg-primary-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-primary-700"
          >
            Start Free
          </Link>
          <Link
            href="/auth/login"
            className="rounded-lg border border-gray-300 px-6 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-50"
          >
            Log In
          </Link>
        </div>
        <p className="mt-4 text-xs text-gray-400">
          Free plan includes 50 leads and 10 searches/month. No credit card required.
        </p>
      </div>
    </main>
  );
}
