import { compute, compute2 } from "./day{{num}}"

describe('compute', () => {
    test.each<[any, any]>(
        [
            [
                1,
                2
            ]
        ]
    )('with %p', (input, expected) => {
        expect(compute(input)).toBe(expected)
    })
})

describe('compute2', () => {
    test.each<[any, any]>(
        [
            [
                1,
                2
            ]
        ]
    )('with %p', (input, expected) => {
        expect(compute2(input)).toBe(expected)
    })
})
