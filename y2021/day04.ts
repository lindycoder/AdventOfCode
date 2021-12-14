import * as fs from 'fs';
import { sum, transpose } from './lib/arrays';

export class Card {
    constructor(
        readonly numbers: number[][]
    ) { }
}

export class BingoInput {
    constructor(
        readonly calls: number[],
        readonly cards: Card[]
    ) { }
}

export class CardState {
    constructor(
        private sequences: number[][],
        private repetition: number,  // Times each unmarked number appear in the lists
    ) { }

    static bidirectional(card: Card): CardState {
        return new CardState(
            [
                ...card.numbers,
                ...transpose(card.numbers),
            ],
            2
        )
    }

    applyCall(call: number) {
        for (const seq of this.sequences) {
            const index = seq.indexOf(call)
            if (index >= 0) {
                seq.splice(index, 1)
            }
        }  
    }

    get hasBingo() : boolean {
        return this.sequences.some(arr => arr.length === 0)
    }

    get score() : number {
        return sum(this.sequences.map(arr => sum(arr))) / this.repetition
    }
}

export function parse(input: string): BingoInput {
    const parts = input.trim().split("\n\n")
    const calls = parts.shift()
    return new BingoInput(
        calls.split(',').map((e) => parseInt(e)),
        parts.map((rawCard) => {
            return new Card(
                rawCard.split('\n').map((cardLine) => {
                    return cardLine.split(/\s+/).map((e) => parseInt(e))
                })
            )
        })
    )
}

export function compute(input: BingoInput): number {
    const cardStates = input.cards.map(CardState.bidirectional)

    for (const call of input.calls) {
        cardStates.forEach(cs => cs.applyCall(call))
        for (const cs of cardStates) {
            if (cs.hasBingo) {
                return cs.score * call
            }
        }
    }
}


export function compute2(input: BingoInput): number {
    let cardStates = input.cards.map(CardState.bidirectional)

    for (const call of input.calls) {
        cardStates.forEach(cs => cs.applyCall(call))
        if (cardStates.length > 1) {
            cardStates = cardStates.filter(cs => !cs.hasBingo)
        } else if (cardStates[0].hasBingo) {
            return cardStates[0].score * call
        }
    }
}

if (require.main === module) {
    const fn = process.argv.length < 3 ? compute : compute2
    console.log(fn(parse(fs.readFileSync(module.filename.replace('.ts', '.input.txt'), 'utf8'))))
}