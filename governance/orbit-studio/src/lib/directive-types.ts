export interface DirectiveItem {
  id: string;
  title: string;
  kind: string;
  repo: string;
  topics: string[];
  activation: string;
  tokens: number;
  sourcePath: string;
  sourceUrl: string;
  body: string;
}

export interface DirectiveArchive {
  sourceRepo: string;
  sourceBranch: string;
  publishedAt: string;
  alwaysOnTokenCap: number;
  items: DirectiveItem[];
}
