import Link from "next/link";

export const metadata = {
  title: "Terms of Service - LeadLocal",
};

export default function TermsPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
      <div className="mb-8">
        <Link href="/marketing" className="text-sm text-primary-600 hover:underline">
          &larr; Back to home
        </Link>
      </div>

      <h1 className="text-3xl font-bold text-gray-900">Terms of Service</h1>
      <p className="mt-2 text-sm text-gray-500">Last updated: February 2026</p>

      <div className="mt-10 space-y-8 text-sm leading-relaxed text-gray-600">
        <section>
          <h2 className="text-lg font-semibold text-gray-900">1. Acceptance of Terms</h2>
          <p className="mt-2">
            By accessing or using LeadLocal (&ldquo;the Service&rdquo;), you agree to be bound by these
            Terms of Service (&ldquo;Terms&rdquo;). If you do not agree to these Terms, you may not
            access or use the Service. These Terms apply to all visitors, users, and others
            who access or use the Service.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">2. Description of Service</h2>
          <p className="mt-2">
            LeadLocal is a software-as-a-service (SaaS) platform that enables users to discover
            local businesses, save leads, manage sales pipelines, and track outreach activities.
            The Service integrates with third-party data providers, including Google Places, to
            deliver business information.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">3. Account Registration</h2>
          <p className="mt-2">
            To use the Service, you must create an account by providing accurate and complete
            information. You are responsible for maintaining the confidentiality of your account
            credentials and for all activities that occur under your account. You must notify us
            immediately of any unauthorized use of your account.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">4. Acceptable Use</h2>
          <p className="mt-2">You agree not to use the Service to:</p>
          <ul className="mt-2 list-disc space-y-1 pl-6">
            <li>Violate any applicable law, regulation, or third-party rights</li>
            <li>Send unsolicited bulk communications (spam) using data obtained from the Service</li>
            <li>Scrape, crawl, or use automated means to access the Service beyond normal API usage</li>
            <li>Attempt to gain unauthorized access to the Service or its related systems</li>
            <li>Interfere with or disrupt the integrity or performance of the Service</li>
            <li>Resell, redistribute, or sublicense data obtained from the Service without authorization</li>
            <li>Use the Service for any illegal, fraudulent, or harmful purpose</li>
          </ul>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">5. Data Usage</h2>
          <p className="mt-2">
            The Service provides business data sourced from publicly available information and
            third-party data providers. You acknowledge that this data is provided &ldquo;as is&rdquo;
            and LeadLocal does not guarantee the accuracy, completeness, or timeliness of any
            business data. You are solely responsible for how you use data obtained through the
            Service and must comply with all applicable laws, including data protection and
            anti-spam regulations.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">6. Billing and Payment</h2>
          <p className="mt-2">
            Certain features of the Service require a paid subscription. By selecting a paid plan,
            you agree to pay the applicable fees as described at the time of purchase. Subscriptions
            are billed on a monthly recurring basis. All fees are non-refundable except as
            expressly stated in these Terms or required by applicable law.
          </p>
          <p className="mt-2">
            We reserve the right to change our pricing at any time. If we change pricing for your
            current plan, we will provide at least 30 days&rsquo; notice before the change takes effect.
            Continued use of the Service after a price change constitutes acceptance of the new
            pricing.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">7. Free Trial</h2>
          <p className="mt-2">
            We may offer free trials of paid plans. At the end of a free trial, your account will
            be downgraded to the Free plan unless you subscribe to a paid plan. We reserve the right
            to modify or discontinue free trials at any time.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">8. Intellectual Property</h2>
          <p className="mt-2">
            The Service and its original content, features, and functionality are owned by LeadLocal
            and are protected by international copyright, trademark, patent, trade secret, and other
            intellectual property laws. You may not copy, modify, distribute, sell, or lease any part
            of our Service without prior written consent.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">9. Termination</h2>
          <p className="mt-2">
            We may terminate or suspend your account immediately, without prior notice or liability,
            for any reason, including if you breach these Terms. Upon termination, your right to use
            the Service will cease immediately. You may also cancel your account at any time from
            your account settings.
          </p>
          <p className="mt-2">
            Upon termination, we may delete your account data after a reasonable retention period.
            We recommend exporting your data before canceling your account.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">10. Limitation of Liability</h2>
          <p className="mt-2">
            To the maximum extent permitted by applicable law, in no event shall LeadLocal, its
            directors, employees, partners, agents, suppliers, or affiliates be liable for any
            indirect, incidental, special, consequential, or punitive damages, including without
            limitation loss of profits, data, use, goodwill, or other intangible losses, resulting
            from:
          </p>
          <ul className="mt-2 list-disc space-y-1 pl-6">
            <li>Your access to or use of (or inability to access or use) the Service</li>
            <li>Any conduct or content of any third party on the Service</li>
            <li>Any content obtained from the Service</li>
            <li>Unauthorized access, use, or alteration of your transmissions or content</li>
          </ul>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">11. Disclaimer</h2>
          <p className="mt-2">
            The Service is provided on an &ldquo;AS IS&rdquo; and &ldquo;AS AVAILABLE&rdquo; basis.
            The Service is provided without warranties of any kind, whether express or implied,
            including but not limited to implied warranties of merchantability, fitness for a
            particular purpose, non-infringement, or course of performance.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">12. Changes to Terms</h2>
          <p className="mt-2">
            We reserve the right to modify or replace these Terms at any time. If a revision is
            material, we will provide at least 30 days&rsquo; notice prior to any new terms taking
            effect. What constitutes a material change will be determined at our sole discretion.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">13. Contact</h2>
          <p className="mt-2">
            If you have any questions about these Terms, please contact us at{" "}
            <a href="mailto:legal@leadlocal.app" className="text-primary-600 hover:underline">
              legal@leadlocal.app
            </a>
            .
          </p>
        </section>
      </div>
    </div>
  );
}
