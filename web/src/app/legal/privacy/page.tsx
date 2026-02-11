import Link from "next/link";

export const metadata = {
  title: "Privacy Policy - LeadLocal",
};

export default function PrivacyPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
      <div className="mb-8">
        <Link href="/marketing" className="text-sm text-primary-600 hover:underline">
          &larr; Back to home
        </Link>
      </div>

      <h1 className="text-3xl font-bold text-gray-900">Privacy Policy</h1>
      <p className="mt-2 text-sm text-gray-500">Last updated: February 2026</p>

      <div className="mt-10 space-y-8 text-sm leading-relaxed text-gray-600">
        <section>
          <h2 className="text-lg font-semibold text-gray-900">1. Introduction</h2>
          <p className="mt-2">
            LeadLocal (&ldquo;we&rdquo;, &ldquo;our&rdquo;, or &ldquo;us&rdquo;) is committed to
            protecting your privacy. This Privacy Policy explains how we collect, use, disclose,
            and safeguard your information when you use our web application and related services
            (collectively, the &ldquo;Service&rdquo;).
          </p>
          <p className="mt-2">
            By using the Service, you consent to the data practices described in this policy. If
            you do not agree with the terms of this Privacy Policy, please do not access or use
            the Service.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">2. Information We Collect</h2>

          <h3 className="mt-4 font-semibold text-gray-800">2.1 Information You Provide</h3>
          <ul className="mt-2 list-disc space-y-1 pl-6">
            <li>
              <strong>Account information:</strong> When you register, we collect your email
              address, full name, and optionally your company name.
            </li>
            <li>
              <strong>Payment information:</strong> If you subscribe to a paid plan, payment
              details are processed by our third-party payment processor. We do not store your
              full credit card number on our servers.
            </li>
            <li>
              <strong>User content:</strong> Notes, tags, and other content you create within
              the Service.
            </li>
          </ul>

          <h3 className="mt-4 font-semibold text-gray-800">2.2 Information Collected Automatically</h3>
          <ul className="mt-2 list-disc space-y-1 pl-6">
            <li>
              <strong>Usage data:</strong> We collect information about how you interact with the
              Service, including pages visited, features used, search queries, and timestamps.
            </li>
            <li>
              <strong>Device information:</strong> Browser type, operating system, IP address,
              and device identifiers.
            </li>
            <li>
              <strong>Log data:</strong> Server logs that may include your IP address, browser
              type, referring/exit pages, and date/time stamps.
            </li>
          </ul>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">3. How We Use Your Information</h2>
          <p className="mt-2">We use the information we collect to:</p>
          <ul className="mt-2 list-disc space-y-1 pl-6">
            <li>Provide, maintain, and improve the Service</li>
            <li>Process transactions and send related information</li>
            <li>Send administrative messages, updates, and security alerts</li>
            <li>Respond to your comments, questions, and support requests</li>
            <li>Monitor and analyze usage trends to improve user experience</li>
            <li>Detect, prevent, and address technical issues and fraud</li>
            <li>Comply with legal obligations</li>
          </ul>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">4. Cookies and Tracking Technologies</h2>
          <p className="mt-2">
            We use cookies and similar tracking technologies to track activity on our Service
            and hold certain information. Cookies are small data files stored on your device.
          </p>
          <ul className="mt-2 list-disc space-y-1 pl-6">
            <li>
              <strong>Essential cookies:</strong> Required for the Service to function properly,
              including authentication and session management.
            </li>
            <li>
              <strong>Analytics cookies:</strong> Help us understand how users interact with the
              Service so we can improve it.
            </li>
          </ul>
          <p className="mt-2">
            You can instruct your browser to refuse all cookies or to indicate when a cookie is
            being sent. However, some features of the Service may not function properly without
            cookies.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">5. Third-Party Services</h2>
          <p className="mt-2">
            We may share your information with third-party service providers that perform services
            on our behalf, including:
          </p>
          <ul className="mt-2 list-disc space-y-1 pl-6">
            <li>
              <strong>Payment processing:</strong> We use third-party payment processors to handle
              subscription billing securely.
            </li>
            <li>
              <strong>Analytics:</strong> We may use analytics services to monitor and analyze
              Service usage.
            </li>
            <li>
              <strong>Data providers:</strong> We use Google Places API and other data providers
              to deliver business search results. Your search queries may be shared with these
              providers.
            </li>
            <li>
              <strong>Infrastructure:</strong> We use cloud hosting providers to store and
              process data.
            </li>
          </ul>
          <p className="mt-2">
            These third parties have access to your information only to perform specific tasks on
            our behalf and are obligated not to disclose or use it for any other purpose.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">6. Data Security</h2>
          <p className="mt-2">
            We implement appropriate technical and organizational security measures to protect
            your personal information against unauthorized access, alteration, disclosure, or
            destruction. These measures include encryption in transit (TLS), secure password
            hashing, and access controls. However, no method of transmission over the Internet
            or method of electronic storage is 100% secure.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">7. Data Retention</h2>
          <p className="mt-2">
            We retain your personal information for as long as your account is active or as needed
            to provide you with the Service. If you delete your account, we will delete or
            anonymize your personal data within 30 days, except where we are required to retain
            it for legal, accounting, or reporting obligations.
          </p>
          <p className="mt-2">
            Lead data, notes, and other user-generated content are retained for the duration of
            your subscription and deleted within 30 days of account termination.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">8. Your Rights (GDPR)</h2>
          <p className="mt-2">
            If you are a resident of the European Economic Area (EEA), you have certain data
            protection rights under the General Data Protection Regulation (GDPR). These include:
          </p>
          <ul className="mt-2 list-disc space-y-1 pl-6">
            <li>
              <strong>Right to access:</strong> You can request a copy of the personal data we
              hold about you.
            </li>
            <li>
              <strong>Right to rectification:</strong> You can request that we correct any
              inaccurate or incomplete data.
            </li>
            <li>
              <strong>Right to erasure:</strong> You can request that we delete your personal
              data, subject to certain conditions.
            </li>
            <li>
              <strong>Right to restrict processing:</strong> You can request that we limit the
              processing of your data.
            </li>
            <li>
              <strong>Right to data portability:</strong> You can request a machine-readable copy
              of your data.
            </li>
            <li>
              <strong>Right to object:</strong> You can object to the processing of your personal
              data in certain circumstances.
            </li>
          </ul>
          <p className="mt-2">
            To exercise any of these rights, please contact us at{" "}
            <a href="mailto:privacy@leadlocal.app" className="text-primary-600 hover:underline">
              privacy@leadlocal.app
            </a>
            . We will respond to your request within 30 days.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">9. California Privacy Rights</h2>
          <p className="mt-2">
            If you are a California resident, you may have additional rights under the California
            Consumer Privacy Act (CCPA), including the right to know what personal information we
            collect, the right to request deletion, and the right to opt-out of the sale of
            personal information. We do not sell personal information to third parties.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">10. Children&rsquo;s Privacy</h2>
          <p className="mt-2">
            The Service is not intended for individuals under the age of 16. We do not knowingly
            collect personal information from children under 16. If we become aware that we have
            collected personal data from a child under 16, we will take steps to delete that
            information.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">11. Changes to This Privacy Policy</h2>
          <p className="mt-2">
            We may update this Privacy Policy from time to time. We will notify you of any changes
            by posting the new Privacy Policy on this page and updating the &ldquo;Last
            updated&rdquo; date. You are advised to review this Privacy Policy periodically for
            any changes.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900">12. Contact Us</h2>
          <p className="mt-2">
            If you have any questions about this Privacy Policy or our data practices, please
            contact us at:
          </p>
          <ul className="mt-2 list-none space-y-1">
            <li>
              Email:{" "}
              <a href="mailto:privacy@leadlocal.app" className="text-primary-600 hover:underline">
                privacy@leadlocal.app
              </a>
            </li>
          </ul>
        </section>
      </div>
    </div>
  );
}
