import { compute, compute2 } from "./day03"

describe('compute', () => {
    test.each<[string[], number]>(
        [
            [
                [
                    '00100',
                    '11110',
                    '10110',
                    '10111',
                    '10101',
                    '01111',
                    '00111',
                    '11100',
                    '10000',
                    '11001',
                    '00010',
                    '01010',
                ],
                198
            ]
        ]
    )('with %p', (input, expected) => {
        expect(compute(input)).toBe(expected)
    })
})

describe('compute2', () => {
    test.each<[string[], number]>(
        [
            [
                [
                    '00100',
                    '11110',
                    '10110',
                    '10111',
                    '10101',
                    '01111',
                    '00111',
                    '11100',
                    '10000',
                    '11001',
                    '00010',
                    '01010',
                ],
                230
            ]
        ]
    )('with %p', (input, expected) => {
        expect(compute2(input)).toBe(expected)
    })
})
