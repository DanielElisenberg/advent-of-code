import fs from "fs";
import { aperture } from "ramda";

const datastream = fs
  .readFileSync("src/day06/input")
  .toString("utf-8")
  .split("");

const startOfPacket = aperture(4, datastream)
  .map((window, index) => ([...new Set(window)].length == 4 ? index + 4 : null))
  .filter((index) => index != null)[0];
console.log("Part 1: " + startOfPacket);

const startOfMessage = aperture(14, datastream)
  .map((window, index) =>
    [...new Set(window)].length == 14 ? index + 14 : null
  )
  .filter((index) => index != null)[0];
console.log("Part 2: " + startOfMessage);
