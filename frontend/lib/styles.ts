export type StylePreset = {
  id: string;
  label: string;
  style: string;
  lensFeel: string;
  lighting: string;
  colorPalette: string;
  negativePrompt: string;
};

export const STYLE_PRESETS: Record<string, StylePreset> = {
  cinematic_realism: {
    id: "cinematic_realism",
    label: "Cinematic Realism",
    style: "cinematic realism",
    lensFeel: "35mm film texture",
    lighting: "motivated practical lighting",
    colorPalette: "rich neutrals with warm highlights",
    negativePrompt: "plastic skin, over-sharpening, video noise",
  },
  neo_noir: {
    id: "neo_noir",
    label: "Neo-Noir",
    style: "neo-noir",
    lensFeel: "anamorphic flare",
    lighting: "high-contrast chiaroscuro",
    colorPalette: "teal shadows, amber accents",
    negativePrompt: "flat contrast, blown highlights",
  },
  dreamy_anime: {
    id: "dreamy_anime",
    label: "Dreamy Anime",
    style: "dreamy anime illustration",
    lensFeel: "soft depth compression",
    lighting: "ethereal bloom",
    colorPalette: "pastel gradients",
    negativePrompt: "muddy lines, grainy edges",
  },
  documentary: {
    id: "documentary",
    label: "Documentary",
    style: "grounded documentary",
    lensFeel: "handheld vérité",
    lighting: "available light",
    colorPalette: "true-to-life muted tones",
    negativePrompt: "over-stylized bokeh, beauty retouch",
  },
};

export const stylePresetList = Object.values(STYLE_PRESETS);
