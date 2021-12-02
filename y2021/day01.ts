import * as fs from 'fs';

export function parse(input: string) {
    return input.trim().split("\n").map((e) => parseInt(e))
}

export function compute(input: readonly number[]) {
    let counter = 0;
    for (let i = 0; i < input.length - 1; i++) {
        counter += input[i] < input[i + 1] ? 1 : 0
    }
    return counter
}

export function compute2(input: readonly number[]) {
    let windows = [];
    for (let i = 0; i < input.length - 2; i++) {
        windows.push(input.slice(i, i + 3).reduce((a, b) => a + b, 0))
    }
    return compute(windows)
}

if (require.main === module) {
    const fn = process.argv.length < 3 ? compute : compute2 
    console.log(fn(parse(fs.readFileSync(module.filename.replace('.ts', '.input.txt'), 'utf8'))))
}