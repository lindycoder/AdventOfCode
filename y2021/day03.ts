import * as fs from 'fs';
import { distribution, transpose } from './lib/arrays';

export function parse(input: string): string[] {
    return input.trim().split("\n").map((e) => e)
}

export function compute(input: string[]): number {
    const transposed = transpose(input.map((e) => e.split('')))
    const [gamma, epsilon] = transposed.reduce(([gamma, epsilon], line) => {
        const dist = distribution(line)
        if (dist['0'] < dist['1']) {
            epsilon += '0';
            gamma += '1';
        } else {
            epsilon += '1';
            gamma += '0';
        }
        return [gamma, epsilon]
    }, ['', ''])

    return parseInt(gamma, 2) * parseInt(epsilon, 2)
}

type Filter = (a: string) => boolean;

const ZEROS: Filter = (e) => e === '0';
const ONES: Filter = (e) => e === '1';

export function compute2(input: string[]): number {
    const o2 = find_rating(input, (dist) => dist['1'] >= dist['0'] ? ONES : ZEROS)
    const co2 = find_rating(input, (dist) => dist['0'] <= dist['1'] ? ZEROS : ONES)
    return o2 * co2;
}

function find_rating(input: string[], getFilter: (dist: Record<string, number>) => Filter): number {
    let remaining: string[][] = input.map((e) => e.split(''));
    let index = 0;
    while (remaining.length > 1) {
        const dist = distribution(transpose(remaining)[index])
        const valFilter = getFilter(dist)
        remaining = remaining.filter((e) => valFilter(e[index]))
        index += 1;
    }
    return parseInt(remaining[0].join(''), 2)
}

if (require.main === module) {
    const fn = process.argv.length < 3 ? compute : compute2
    console.log(fn(parse(fs.readFileSync(module.filename.replace('.ts', '.input.txt'), 'utf8'))))
}