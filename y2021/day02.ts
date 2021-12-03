import * as fs from 'fs';

const directions = <const>['forward', 'down', 'up'];
export type Direction = typeof directions[number]
function isDir(str: string): str is Direction {
    return !!directions.find((dir) => str === dir);
}

export interface Step {
    direction: Direction
    amount: number
}

export function parse(input: string): Step[] {
    return input.trim().split("\n").map((e) => {
        const [direction, amount] = e.split(' ', 2)
        if (isDir(direction)) {
            return { direction, amount: parseInt(amount) }
        }
        throw `What is ${direction}?`
    })
}

type Operations = {
    [key in Direction]: (pos: Pos, amount: number) => Pos;
};

const op: Operations = {
    'forward': (pos, amount) => Object.assign({}, pos, {x: pos.x + amount}),
    'down': (pos, amount) => Object.assign({}, pos, {y: pos.y + amount}),
    'up': (pos, amount) => Object.assign({}, pos, {y: pos.y - amount}),
}

interface Pos {
    readonly x: number
    readonly y: number
}

export function compute(input: Step[]): string | number {
    let pos = { x: 0, y: 0 }
    for (const step of input) {
        pos = op[step.direction](pos, step.amount)
    }
    return pos.x * pos.y
}


type OperationsAim = {
    [key in Direction]: (pos: PosAim, amount: number) => PosAim;
};

const opAim: OperationsAim = {
    'forward': (pos, amount) => Object.assign({}, pos, {
        x: pos.x + amount, 
        y: pos.y + (amount * pos.aim)
    }),
    'down': (pos, amount) => Object.assign({}, pos, {aim: pos.aim + amount}),
    'up': (pos, amount) => Object.assign({}, pos, {aim: pos.aim - amount}),
}

interface PosAim {
    readonly x: number
    readonly y: number
    readonly aim: number
}

export function compute2(input: Step[]): string | number {
    let pos = { x: 0, y: 0, aim: 0 }
    for (const step of input) {
        pos = opAim[step.direction](pos, step.amount)
    }
    return pos.x * pos.y
}

if (require.main === module) {
    const fn = process.argv.length < 3 ? compute : compute2
    console.log(fn(parse(fs.readFileSync(module.filename.replace('.ts', '.input.txt'), 'utf8'))))
}