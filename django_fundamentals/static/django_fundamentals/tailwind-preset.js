/**
 * SHARED TAILWIND PRESET FOR PROJECTS BUILT ON django-fundamentals.
 *
 * THIS FILE OWNS THE *MAPPING* FROM SEMANTIC UTILITY NAMES ONTO CSS CUSTOM
 * PROPERTIES. THE HOST PROJECT OWNS THE *VALUES*, IN static/src/tokens.css.
 *
 * IT LIVES IN THE PACKAGE (RATHER THAN IN THE GENERATED PROJECT'S
 * tailwind.config.js) SO THAT IMPROVEMENTS REACH EXISTING APPS VIA
 * `pip install -U django-fundamentals` — A GENERATED PROJECT'S OWN CONFIG
 * FILES NEVER RECEIVE UPDATES.
 *
 * COLOURS RESOLVE THROUGH rgb(var(--x) / <alpha-value>) SO THAT TAILWIND
 * OPACITY MODIFIERS (bg-brand/10, text-ink/70) KEEP WORKING.
 */

/** BUILD A COLOUR THAT SUPPORTS TAILWIND'S OPACITY MODIFIER SYNTAX. */
function tokenColor(variableName) {
  return ({ opacityValue }) =>
    opacityValue === undefined
      ? `rgb(var(${variableName}))`
      : `rgb(var(${variableName}) / ${opacityValue})`;
}

/**
 * BASE STYLES FOR FORM CONTROLS.
 *
 * REGISTERED AS ELEMENT-LEVEL BASE STYLES RATHER THAN UTILITY CLASSES ON
 * PURPOSE: django-allauth RENDERS ITS OWN FORM WIDGETS AND WE ONLY OVERRIDE A
 * SUBSET OF ITS TEMPLATES, SO ANY PAGE WE HAVEN'T TOUCHED STILL GETS PROPERLY
 * STYLED INPUTS FOR FREE.
 */
// DECLARED AS A BARE FUNCTION RATHER THAN VIA tailwindcss/plugin ON PURPOSE:
// THIS FILE IS LOADED FROM PYTHON'S site-packages, WHICH HAS NO node_modules
// ABOVE IT, SO ANY require("tailwindcss/...") HERE FAILS TO RESOLVE. TAILWIND
// ACCEPTS A PLAIN HANDLER FUNCTION IN `plugins`, SO NO IMPORT IS NEEDED.
const formControls = ({ addBase, theme }) => {
  const control = {
    width: "100%",
    borderRadius: "var(--radius)",
    borderWidth: "1px",
    borderColor: "rgb(var(--color-line))",
    backgroundColor: "rgb(var(--color-surface))",
    color: "rgb(var(--color-ink))",
    paddingInline: theme("spacing.3"),
    paddingBlock: theme("spacing.2"),
    fontSize: theme("fontSize.sm[0]"),
    lineHeight: theme("fontSize.sm[1].lineHeight"),
    "&::placeholder": { color: "rgb(var(--color-muted))" },
    "&:focus": {
      outline: "none",
      borderColor: "rgb(var(--color-brand))",
      boxShadow: "0 0 0 2px rgb(var(--color-brand) / 0.25)",
    },
    "&:disabled": { opacity: "0.5", cursor: "not-allowed" },
  };

  addBase({
    // ALPINE'S x-cloak IS INERT WITHOUT THIS RULE — ELEMENTS WAITING ON ALPINE
    // WOULD FLASH VISIBLE BEFORE IT BOOTS (BOTH THEME ICONS AT ONCE, THE
    // MOBILE SIDEBAR, DROPDOWN MENUS).
    "[x-cloak]": { display: "none !important" },

    [[
      'input[type="text"]',
      'input[type="email"]',
      'input[type="password"]',
      'input[type="url"]',
      'input[type="tel"]',
      'input[type="number"]',
      'input[type="search"]',
      'input[type="date"]',
      "select",
      "textarea",
    ].join(", ")]: control,

    // NATIVE CHECKBOXES/RADIOS IGNORE `color`; accent-color IS THE PROPERTY
    // BROWSERS ACTUALLY HONOUR, AND AVOIDS HAVING TO REBUILD THE CONTROL WITH
    // appearance:none (WHICH WOULD ALSO LOSE THE INDETERMINATE STATE).
    'input[type="checkbox"], input[type="radio"]': {
      width: "1rem",
      height: "1rem",
      accentColor: "rgb(var(--color-brand))",
      borderColor: "rgb(var(--color-line))",
      cursor: "pointer",
      "&:focus-visible": {
        outline: "2px solid rgb(var(--color-brand))",
        outlineOffset: "2px",
      },
    },

    // DJANGO AND allauth BOTH RENDER FORM ERRORS AS <ul class="errorlist">.
    // STYLING IT HERE COVERS FORMS WE DON'T RENDER OURSELVES.
    //
    // NOTE: TAILWIND PURGES addBase RULES WHOSE SELECTOR NAMES A CLASS THAT
    // NEVER APPEARS IN SCANNED CONTENT — AND "errorlist" IS NORMALLY ONLY
    // EMITTED AT RUNTIME. molecules/form_field.html WRITES THE CLASS LITERALLY
    // SO THIS RULE SURVIVES THE BUILD. DON'T REMOVE IT THERE.
    "ul.errorlist": {
      listStyle: "none",
      margin: "0.375rem 0 0 0",
      padding: "0",
      fontSize: theme("fontSize.xs[0]"),
      color: "rgb(var(--color-danger))",
    },
  });
};

module.exports = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // SURFACES
        surface: tokenColor("--color-surface"),
        raised: tokenColor("--color-raised"),
        sunken: tokenColor("--color-sunken"),
        // TEXT
        ink: tokenColor("--color-ink"),
        muted: tokenColor("--color-muted"),
        // ACCENT
        brand: {
          DEFAULT: tokenColor("--color-brand"),
          fg: tokenColor("--color-brand-fg"),
          muted: tokenColor("--color-brand-muted"),
        },
        // BORDERS + FEEDBACK
        line: tokenColor("--color-line"),
        success: tokenColor("--color-success"),
        warning: tokenColor("--color-warning"),
        danger: tokenColor("--color-danger"),
      },
      spacing: {
        sidebar: "var(--sidebar-w)",
        navbar: "var(--navbar-h)",
      },
      width: { sidebar: "var(--sidebar-w)" },
      height: { navbar: "var(--navbar-h)" },
      minHeight: { navbar: "var(--navbar-h)" },
      maxWidth: {
        content: "var(--content-max)",
        shell: "var(--shell-max)",
      },
      borderRadius: {
        DEFAULT: "var(--radius)",
        lg: "var(--radius-lg)",
      },
      fontFamily: {
        sans: "var(--font-sans)",
        mono: "var(--font-mono)",
      },
      zIndex: {
        sidebar: "var(--z-sidebar)",
        navbar: "var(--z-navbar)",
        overlay: "var(--z-overlay)",
      },
    },
  },
  plugins: [formControls],
};
