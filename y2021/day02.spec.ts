import { compute, compute2, Direction } from "./day02"

const d: Direction = 'forward'

describe('compute', () => {
    test.each<[[Direction, number][], any]>(
        [
            [
                [
                    ['forward', 5],
                    ['down', 5],
                    ['forward', 8],
                    ['up', 3],
                    ['down', 8],
                    ['forward', 2],
                ],
                150
            ],
        ]
    )('with %p', (input, expected) => {
        expect(compute(input.map(([direction, amount]) => ({ direction, amount })))).toBe(expected)
    })
})

describe('compute2', () => {
    test.each<[[Direction, number][], any]>(
        [
            [
                [
                    ['forward', 5],
                    ['down', 5],
                    ['forward', 8],
                    ['up', 3],
                    ['down', 8],
                    ['forward', 2],
                ],
                900
            ],
        ]
    )('with %p', (input, expected) => {
        expect(compute2(input.map(([direction, amount]) => ({ direction, amount })))).toBe(expected)
    })
})
