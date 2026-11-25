import { votes, speeches, meta } from "./data";
// One id per build; pages embed it and compare with /version.json to detect a newer deploy.
export const BUILD_ID = new Date().toISOString();
export const versionInfo = { v: BUILD_ID, updatedAt: meta.updatedAt, votes: votes.length, speeches: speeches.length };
