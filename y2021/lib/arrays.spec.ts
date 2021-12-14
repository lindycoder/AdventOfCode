import { distribution, list, sum, transpose, zip } from './arrays'

describe('list', () => {
    it('should convert an iterator to an array', () => {
        function* func() {
            yield 1
            yield 2
        }
        expect(list(func())).toStrictEqual([1, 2])
    })
    it('should support empty arrays', () => {
        function* func() {}
        expect(list(func())).toStrictEqual([])
    })
})

describe('zip', () => {
    it.each<[any[], any[], any[]]>([
        [
            [],
            [],
            []
        ],
        [
            [1],
            ["a"],
            [
                [1, "a"]
            ]
        ],
        [
            [1, 2],
            ["a", "b"],
            [
                [1, "a"],
                [2, "b"],
            ]
        ],
    ])('should zip %p, %p', (a, b, matches) => {
        const z = list(zip(a, b))
        expect(z).toStrictEqual(matches)
    })
})

describe('transpose', () => {
    it.each<[any[][], any[][]]>([
        [
            [],
            []
        ],
        [
            [[1]],
            [[1]]
        ],
        [
            [
                [1, 2, 3], 
                [1, 2, 3], 
            ],
            [
                [1, 1],
                [2, 2],
                [3, 3],
            ]
        ],
    ])('should transpose %p to %p', (input, matches) => {
        const z = transpose(input)
        expect(z).toStrictEqual(matches)
    })
})

describe('distribution', () => {
    it.each<[string[], Record<string, number>]>([
        [
            [],
            {}
        ],
        [
            ['a', 'b', 'a'],
            {
                'a': 2,
                'b': 1
            }
        ],
    ])('should plot the distribution of %p', (input, matches) => {
        const z = distribution(input)
        expect(z).toStrictEqual(matches)
    })
})

describe('sum', () => {
    it.each<[number[], number]>([
        [
            [],
            0
        ],
        [
            [1],
            1
        ],
        [
            [1, 2, 3],
            6
        ],
    ])('should add all items together: %p', (input, matches) => {
        expect(sum(input)).toStrictEqual(matches)
    })
})