import * as fs from 'fs';

export function parse(input: string): string[] {
    return input.trim().split("\n").map((e) => e)
}

export function compute(input: string[]): string | number  {
    return ''
}

export function compute2(input: string[]): string | number {
    return ''
}

if (require.main === module) {
    const fn = process.argv.length < 3 ? compute : compute2 
    console.log(fn(parse(fs.readFileSync(module.filename.replace('.ts', '.input.txt'), 'utf8'))))
}