// JSON for <script type="application/json">: escape <, >, & and line separators so text from nrsr.sk can never close the tag.
export const safeJson = (v: unknown) =>
  JSON.stringify(v).replace(/</g, "\\u003c").replace(/>/g, "\\u003e").replace(/&/g, "\\u0026").replace(/\u2028/g, "\\u2028").replace(/\u2029/g, "\\u2029");
