import fs from "fs";

let path: string[] = ["/"];
const sizes: { [id: string]: number } = { "/": 0 };

fs.readFileSync("src/day07/input")
  .toString("utf-8")
  .split("\n")
  .filter((line) => line != "")
  .slice(1)
  .filter((line) => !line.startsWith("$ ls") && !line.startsWith("dir"))
  .map((line) => line.split(" "))
  .forEach((line) => {
    if (line[1] == "cd" && line[2] == "..") {
      path = path.slice(0, path.length - 1);
    } else if (line[1] == "cd") {
      path = path.concat([line[2] + "/"]);
    } else {
      let containsPath = "";
      path.forEach((subpath) => {
        containsPath = containsPath.concat(subpath);
        if (!(containsPath in sizes)) {
          sizes[containsPath] = 0;
        }
        sizes[containsPath] = sizes[containsPath] + parseInt(line[0]);
      });
    }
  });
const directorySum = Object.values(sizes)
  .filter((size) => size <= 100000)
  .reduce((a, b) => a + b, 0);
console.log("Part 1: " + directorySum);
const unusedSpace = 70000000 - sizes["/"];
const neededSpace = 30000000 - unusedSpace;
const deletedDirectory = Math.min(
  ...Object.values(sizes).filter((size) => size >= neededSpace)
);
console.log("Part 2: " + deletedDirectory);
