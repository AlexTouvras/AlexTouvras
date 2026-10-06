import { readFile } from "node:fs/promises";
import path from "node:path";
import { NextResponse } from "next/server";
import { isStudioAccessible } from "@/lib/auth";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const ROOT = path.join(process.cwd(), "data", "studio-daycare");

const TYPES: Record<string, string> = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
};

export async function GET(
  _request: Request,
  context: { params: Promise<{ path?: string[] }> },
) {
  if (!(await isStudioAccessible())) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const parts = (await context.params).path ?? ["index.html"];
  if (
    parts.some(
      (part) => part === "" || part === "." || part === ".." || part.includes("/") || part.includes("\\"),
    )
  ) {
    return new NextResponse("Not found", { status: 404 });
  }

  const root = path.resolve(ROOT);
  const file = path.resolve(root, ...parts);
  if (file !== root && !file.startsWith(root + path.sep)) {
    return new NextResponse("Not found", { status: 404 });
  }

  const type = TYPES[path.extname(file)];
  if (!type) return new NextResponse("Not found", { status: 404 });

  try {
    const body = await readFile(file);
    return new NextResponse(body, {
      headers: {
        "Content-Type": type,
        "Cache-Control": "private, no-store",
        "X-Robots-Tag": "noindex, nofollow",
      },
    });
  } catch {
    return new NextResponse("Not found", { status: 404 });
  }
}
