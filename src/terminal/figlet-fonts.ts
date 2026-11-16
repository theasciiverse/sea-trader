import figlet from "figlet";
import small from "figlet/importable-fonts/Small.js";
import standard from "figlet/importable-fonts/Standard.js";

// The fonts are parsed from the imported files, so figlet never looks for
// them on disk and the game also runs as a single bundled executable.
figlet.parseFont("Small", small);
figlet.parseFont("Standard", standard);

/** Big lettering for a screen title, with an empty line above and below. */
export const bigText = (text: string) => `\n${figlet.textSync(text, { font: "Small", horizontalLayout: "full" })}\n`;

export const titleText = (text: string) => figlet.textSync(text, { font: "Standard" });
