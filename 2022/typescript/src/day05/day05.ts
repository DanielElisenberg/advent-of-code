import fs from "fs";

enum Method {
  OneByOne,
  All,
}

const doMoves = (
  stacks: Array<Array<string>>,
  moves: string[],
  method: Method
): string => {
  const mutableStacks = JSON.parse(JSON.stringify(stacks));
  moves.forEach((move) => {
    const amount = parseInt(move.split(" ")[1]);
    const fromStack = parseInt(move.split(" ")[3]) - 1;
    const toStack = parseInt(move.split(" ")[5]) - 1;
    const crates = mutableStacks[fromStack].slice(0, amount);
    mutableStacks[fromStack] = mutableStacks[fromStack].slice(
      amount,
      mutableStacks[fromStack].length
    );
    switch (method) {
      case Method.OneByOne: {
        mutableStacks[toStack] = [
          ...crates.reverse(),
          ...mutableStacks[toStack],
        ];
        break;
      }
      case Method.All: {
        mutableStacks[toStack] = [...crates, ...mutableStacks[toStack]];
        break;
      }
    }
  });
  return mutableStacks.map((stack) => stack[0]).join("");
};

const lines = fs
  .readFileSync("src/day05/input")
  .toString("utf-8")
  .split("\n")
  .filter((line) => line != "");

const moves = lines.slice(9);
const stacks = [...Array(9).keys()].map((stack) => {
  return [...Array(8).keys()]
    .reverse()
    .map((crate) => lines[crate][stack * 4 + 1])
    .filter((crate) => crate !== " ")
    .reverse();
});

console.log("Part 1: " + doMoves(stacks, moves, Method.OneByOne));
console.log("Part 1: " + doMoves(stacks, moves, Method.All));
