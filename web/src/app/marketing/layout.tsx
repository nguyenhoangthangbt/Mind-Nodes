import Link from "next/link";

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link href="/marketing" className="text-xl font-bold tracking-tight text-gray-900">
            Lead<span className="text-primary-600">Local</span>
          </Link>

          <nav className="flex items-center gap-8">
            <Link
              href="/marketing#features"
              className="text-sm font-medium text-gray-600 hover:text-gray-900"
            >
              Features
            </Link>
            <Link
              href="/marketing/pricing"
              className="text-sm font-medium text-gray-600 hover:text-gray-900"
            >
              Pricing
            </Link>
            <Link
              href="/auth/login"
              className="text-sm font-medium text-gray-600 hover:text-gray-900"
            >
              Login
            </Link>
            <Link
              href="/auth/signup"
              className="rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700"
            >
              Start Free
            </Link>
          </nav>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1">{children}</main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-gray-50">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            {/* Brand */}
            <div className="col-span-2 md:col-span-1">
              <span className="text-lg font-bold text-gray-900">
                Lead<span className="text-primary-600">Local</span>
              </span>
              <p className="mt-2 text-sm text-gray-500">
                Discover local businesses, build your pipeline, and close more deals.
              </p>
            </div>

            {/* Product */}
            <div>
              <h4 className="text-sm font-semibold text-gray-900">Product</h4>
              <ul className="mt-3 space-y-2">
                <li>
                  <Link href="/marketing#features" className="text-sm text-gray-500 hover:text-gray-700">
                    Features
                  </Link>
                </li>
                <li>
                  <Link href="/marketing/pricing" className="text-sm text-gray-500 hover:text-gray-700">
                    Pricing
                  </Link>
                </li>
              </ul>
            </div>

            {/* Company */}
            <div>
              <h4 className="text-sm font-semibold text-gray-900">Company</h4>
              <ul className="mt-3 space-y-2">
                <li>
                  <Link href="/legal/terms" className="text-sm text-gray-500 hover:text-gray-700">
                    Terms of Service
                  </Link>
                </li>
                <li>
                  <Link href="/legal/privacy" className="text-sm text-gray-500 hover:text-gray-700">
                    Privacy Policy
                  </Link>
                </li>
              </ul>
            </div>

            {/* Support */}
            <div>
              <h4 className="text-sm font-semibold text-gray-900">Support</h4>
              <ul className="mt-3 space-y-2">
                <li>
                  <a href="mailto:support@leadlocal.app" className="text-sm text-gray-500 hover:text-gray-700">
                    Contact Us
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="mt-8 border-t border-gray-200 pt-8">
            <p className="text-center text-xs text-gray-400">
              &copy; {new Date().getFullYear()} LeadLocal. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
