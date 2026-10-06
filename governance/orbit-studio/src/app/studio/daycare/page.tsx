import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { isStudioAccessible } from "@/lib/auth";

export const metadata: Metadata = {
  title: "Studio · Daycare",
  robots: { index: false, follow: false },
};

export const dynamic = "force-dynamic";

export default async function StudioDaycarePage() {
  if (!(await isStudioAccessible())) redirect("/studio/login");

  return (
    <div className="fixed inset-0 z-[60] flex flex-col bg-[#f3efe6]">
      <div className="flex items-center justify-between gap-3 border-b border-[#e3dacb] px-4 py-2 text-sm text-[#1c2430]">
        <Link
          href="/studio"
          className="font-medium underline-offset-2 hover:underline"
        >
          Back to Studio
        </Link>
        <p className="text-[#5c564c]">
          Temporary daycare shortlist. Not on the public site.
        </p>
      </div>
      <iframe
        title="Daycare comparison"
        src="/studio/daycare/site/index.html"
        className="min-h-0 w-full flex-1 border-0 bg-[#f3efe6]"
      />
    </div>
  );
}
