import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { DirectiveArchiveBrowser } from "@/components/studio/DirectiveArchive";
import { LogoutButton } from "@/components/studio/LogoutButton";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { isStudioAccessible } from "@/lib/auth";
import { getDirectiveArchive } from "@/lib/directives";

export const metadata: Metadata = {
  title: "Studio · Directives",
  robots: { index: false, follow: false },
};

export default async function StudioDirectivesPage() {
  if (!(await isStudioAccessible())) redirect("/studio/login");

  const archive = getDirectiveArchive();

  return (
    <div>
      <div className="flex items-start justify-between gap-4">
        <div>
          <Link
            href="/studio"
            className="focus-ring mb-4 inline-flex min-h-11 items-center gap-1.5 text-sm text-slate-400 hover:text-neon-cyan"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden />
            Studio
          </Link>
          <SectionHeading
            eyebrow="Studio"
            title="Directives"
            description="Rules, skills, and automation prompts. Private. Not shown on the public site."
          />
        </div>
        <LogoutButton />
      </div>
      <div className="mt-8">
        <DirectiveArchiveBrowser archive={archive} />
      </div>
    </div>
  );
}
