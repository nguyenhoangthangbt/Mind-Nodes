import Link from "next/link";

const tiers = [
  {
    name: "Free",
    price: "$0",
    period: "",
    description: "Get started with the basics.",
    cta: "Start Free",
    href: "/auth/signup",
    popular: false,
    limits: {
      leads: "50 leads",
      searches: "10 searches/mo",
    },
    features: [
      "50 saved leads",
      "10 searches per month",
      "Basic pipeline management",
      "Notes on leads",
      "CSV export",
    ],
  },
  {
    name: "Starter",
    price: "$19",
    period: "/mo",
    description: "For freelancers getting serious.",
    cta: "Start Free Trial",
    href: "/auth/signup?plan=starter",
    popular: false,
    limits: {
      leads: "500 leads",
      searches: "50 searches/mo",
    },
    features: [
      "500 saved leads",
      "50 searches per month",
      "Full pipeline management",
      "Notes & reminders",
      "CSV export",
      "Email support",
    ],
  },
  {
    name: "Pro",
    price: "$39",
    period: "/mo",
    description: "For growing agencies.",
    cta: "Start Free Trial",
    href: "/auth/signup?plan=pro",
    popular: true,
    limits: {
      leads: "2,000 leads",
      searches: "200 searches/mo",
    },
    features: [
      "2,000 saved leads",
      "200 searches per month",
      "Full pipeline management",
      "Notes & reminders",
      "Advanced analytics",
      "CSV export",
      "Priority support",
    ],
  },
  {
    name: "Agency",
    price: "$79",
    period: "/mo",
    description: "For teams that need it all.",
    cta: "Start Free Trial",
    href: "/auth/signup?plan=agency",
    popular: false,
    limits: {
      leads: "10,000 leads",
      searches: "Unlimited searches",
    },
    features: [
      "10,000 saved leads",
      "Unlimited searches",
      "Full pipeline management",
      "Notes & reminders",
      "Advanced analytics",
      "CSV export",
      "Priority support",
      "Dedicated onboarding",
    ],
  },
];

const comparisonFeatures = [
  { name: "Saved leads", free: "50", starter: "500", pro: "2,000", agency: "10,000" },
  { name: "Searches per month", free: "10", starter: "50", pro: "200", agency: "Unlimited" },
  { name: "Pipeline management", free: "Basic", starter: "Full", pro: "Full", agency: "Full" },
  { name: "Notes", free: true, starter: true, pro: true, agency: true },
  { name: "Reminders", free: false, starter: true, pro: true, agency: true },
  { name: "CSV export", free: true, starter: true, pro: true, agency: true },
  { name: "Advanced analytics", free: false, starter: false, pro: true, agency: true },
  { name: "Priority support", free: false, starter: false, pro: true, agency: true },
  { name: "Dedicated onboarding", free: false, starter: false, pro: false, agency: true },
];

const faqs = [
  {
    question: "Is there a free trial?",
    answer:
      "Yes! All paid plans come with a 14-day free trial. No credit card is required to start. You can also use our Free plan indefinitely with limited features.",
  },
  {
    question: "Can I change plans later?",
    answer:
      "Absolutely. You can upgrade or downgrade your plan at any time from your account settings. When upgrading, you will be prorated for the remainder of your billing cycle. When downgrading, the change takes effect at the start of your next billing period.",
  },
  {
    question: "How does billing work?",
    answer:
      "Paid plans are billed monthly. You can cancel anytime and your subscription will remain active until the end of your current billing period. We accept all major credit cards.",
  },
  {
    question: "What happens when I hit my lead or search limit?",
    answer:
      "When you reach your plan's lead limit, you will need to archive or delete existing leads before saving new ones, or upgrade to a higher plan. Search limits reset at the start of each billing cycle.",
  },
  {
    question: "Can I cancel anytime?",
    answer:
      "Yes. There are no long-term contracts or cancellation fees. You can cancel your subscription at any time from your account settings. Your access continues until the end of your current billing period.",
  },
  {
    question: "Do you offer refunds?",
    answer:
      "We offer a full refund within the first 7 days of any paid subscription if you are not satisfied. After that, we do not offer partial refunds, but you can cancel anytime to prevent future charges.",
  },
];

export default function PricingPage() {
  return (
    <>
      {/* Header */}
      <section className="bg-white py-20">
        <div className="mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            Simple, transparent pricing
          </h1>
          <p className="mt-4 text-lg text-gray-600">
            Start free and scale as you grow. No hidden fees, no surprises.
          </p>
        </div>
      </section>

      {/* Pricing cards */}
      <section className="bg-gray-50 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            {tiers.map((tier) => (
              <div
                key={tier.name}
                className={`relative flex flex-col rounded-2xl bg-white p-8 shadow-sm ${
                  tier.popular
                    ? "ring-2 ring-primary-600 shadow-lg"
                    : "border border-gray-200"
                }`}
              >
                {tier.popular && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-primary-600 px-3 py-1 text-xs font-semibold text-white">
                    Most Popular
                  </span>
                )}

                <h3 className="text-lg font-semibold text-gray-900">{tier.name}</h3>
                <p className="mt-1 text-sm text-gray-500">{tier.description}</p>

                <div className="mt-6">
                  <span className="text-4xl font-bold text-gray-900">{tier.price}</span>
                  {tier.period && (
                    <span className="text-sm text-gray-500">{tier.period}</span>
                  )}
                </div>

                <div className="mt-4 flex gap-4 text-xs text-gray-500">
                  <span>{tier.limits.leads}</span>
                  <span>&middot;</span>
                  <span>{tier.limits.searches}</span>
                </div>

                <ul className="mt-6 flex-1 space-y-3">
                  {tier.features.map((feature) => (
                    <li key={feature} className="flex items-start gap-2 text-sm text-gray-600">
                      <svg
                        className="mt-0.5 h-4 w-4 flex-shrink-0 text-primary-600"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={2}
                        stroke="currentColor"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>

                <Link
                  href={tier.href}
                  className={`mt-8 block rounded-lg px-4 py-2.5 text-center text-sm font-semibold ${
                    tier.popular
                      ? "bg-primary-600 text-white hover:bg-primary-700"
                      : "border border-gray-300 text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  {tier.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature comparison table */}
      <section className="bg-white py-20">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center text-2xl font-bold text-gray-900">
            Compare plans
          </h2>

          <div className="mt-12 overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="pb-4 pr-6 font-semibold text-gray-900">Feature</th>
                  <th className="pb-4 px-4 text-center font-semibold text-gray-900">Free</th>
                  <th className="pb-4 px-4 text-center font-semibold text-gray-900">Starter</th>
                  <th className="pb-4 px-4 text-center font-semibold text-primary-600">Pro</th>
                  <th className="pb-4 px-4 text-center font-semibold text-gray-900">Agency</th>
                </tr>
              </thead>
              <tbody>
                {comparisonFeatures.map((feature) => (
                  <tr key={feature.name} className="border-b border-gray-100">
                    <td className="py-3 pr-6 text-gray-700">{feature.name}</td>
                    {(["free", "starter", "pro", "agency"] as const).map((plan) => {
                      const value = feature[plan];
                      return (
                        <td key={plan} className="py-3 px-4 text-center">
                          {typeof value === "boolean" ? (
                            value ? (
                              <svg
                                className="mx-auto h-5 w-5 text-primary-600"
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
                            ) : (
                              <span className="text-gray-300">&mdash;</span>
                            )
                          ) : (
                            <span className="text-gray-700">{value}</span>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="bg-gray-50 py-20">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center text-2xl font-bold text-gray-900">
            Frequently asked questions
          </h2>

          <div className="mt-12 space-y-8">
            {faqs.map((faq) => (
              <div key={faq.question}>
                <h3 className="text-base font-semibold text-gray-900">
                  {faq.question}
                </h3>
                <p className="mt-2 text-sm text-gray-600">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Bottom CTA */}
      <section className="bg-white py-16">
        <div className="mx-auto max-w-4xl px-4 text-center sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-gray-900">
            Ready to start finding leads?
          </h2>
          <p className="mt-3 text-gray-600">
            Start with the Free plan today. No credit card required.
          </p>
          <div className="mt-6">
            <Link
              href="/auth/signup"
              className="inline-block rounded-lg bg-primary-600 px-8 py-3 text-sm font-semibold text-white shadow-sm hover:bg-primary-700"
            >
              Start Free
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
