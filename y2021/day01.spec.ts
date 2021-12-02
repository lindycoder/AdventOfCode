import { compute, compute2 } from "./day01"

describe('compute', () => {
    test.each<[readonly number[], number]>(
        [
            [
                [
                    199,
                    200,
                    208,
                    210,
                    200,
                    207,
                    240,
                    269,
                    260,
                    263,
                ],
                7
            ]
        ]
    )('with %p', (input, expected) => {
        expect(compute(input)).toBe(expected)
    })
})

describe('compute2', () => {
    test.each<[readonly number[], number]>(
        [
            [
                [
                    199,
                    200,
                    208,
                    210,
                    200,
                    207,
                    240,
                    269,
                    260,
                    263,
                ],
                5
            ]
        ]
    )('with %p', (input, expected) => {
        expect(compute2(input)).toBe(expected)
    })
})


