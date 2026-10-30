export const FRAME_COUNT=12;
export const FRAME_COLUMNS=3;
export const FRAME_ROWS=4;
export function frameAt(progress,reducedMotion=false){const value=Number.isFinite(progress)?Math.min(1,Math.max(0,progress)):0;const position=reducedMotion?0:value*(FRAME_COUNT-1);const index=Math.floor(position);return {index,next:Math.min(index+1,FRAME_COUNT-1),blend:position-index};}
