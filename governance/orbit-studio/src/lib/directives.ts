import "server-only";
import fs from "node:fs";
import path from "node:path";
import type { DirectiveArchive, DirectiveItem } from "@/lib/directive-types";

export type { DirectiveArchive, DirectiveItem };

const ARCHIVE_PATH = path.join(process.cwd(), "data", "directive-archive.json");

export function getDirectiveArchive(): DirectiveArchive {
  const raw = fs.readFileSync(ARCHIVE_PATH, "utf8");
  const parsed = JSON.parse(raw) as Partial<DirectiveArchive>;
  return {
    sourceRepo: parsed.sourceRepo ?? "AlexTouvras/AlexTouvras",
    sourceBranch: parsed.sourceBranch ?? "",
    publishedAt: parsed.publishedAt ?? "",
    alwaysOnTokenCap:
      typeof parsed.alwaysOnTokenCap === "number" ? parsed.alwaysOnTokenCap : 1000,
    items: Array.isArray(parsed.items) ? parsed.items : [],
  };
}
