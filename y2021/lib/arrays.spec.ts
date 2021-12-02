import { list, zip } from './arrays'

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
        console.log(z)
        expect(z).toStrictEqual(matches)
    })
})