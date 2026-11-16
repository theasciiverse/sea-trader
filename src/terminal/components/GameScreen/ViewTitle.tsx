import React from "react";
import { Text } from "ink";
import { titleText } from "../../figlet-fonts.js";
import { useScreenSize } from "../../hooks/use-screen-size.js";
import { FULL_TITLE_MIN_HEIGHT } from "../layout.js";

export function ViewTitle({ text }: { text: string }) {
  const { height } = useScreenSize();

  return height >= FULL_TITLE_MIN_HEIGHT ? (
    <Text>{titleText(text)}</Text>
  ) : (
    <Text bold underline>
      {text.toUpperCase()}
    </Text>
  );
}
