var expect = require('chai').expect;

var run_for_real = typeof describe === "undefined";
if (run_for_real) describe = function() {};

var X = [0, 1], Y = [1, 0];

function compute(size_x, size_y, data) {
    var commands = data.split("\n"),
        matrix = new Matrix(size_x, size_y);
        var parts;

    for (var i = 0; i < commands.length; i++) {
        if (parts = /rect (\d+)x(\d+)/.exec(commands[i])) {
            matrix.rect(parts[1], parts[2]);
        } else if (parts = /rotate column x=(\d+) by (\d+)/.exec(commands[i])) {
            matrix.rotate(X, parts[1], parts[2]);
        } else if (parts = /rotate row y=(\d+) by (\d+)/.exec(commands[i])) {
            matrix.rotate(Y, parts[1], parts[2]);
        }
    }

    return matrix.toString();
}

Matrix = function(size_x, size_y) {
    this.state = [];
    for (var y = 0; y < size_y; y++) {
        this.state[y] = [];
        for (var x = 0; x < size_x; x++) {
            this.state[y][x] = 0;
        }
    }
};

Matrix.prototype.rect = function(size_x, size_y) {
    for (var y = 0; y < size_y; y++) {
        for (var x = 0; x < size_x; x++) {
            this.state[y][x] = 1;
        }
    }
};

Matrix.prototype.set_rect = function(size_x, size_y, value) {
    for (var y = 0; y < size_y; y++) {
        for (var x = 0; x < size_x; x++) {
            this.state[y][x] = value;
        }
    }
};

Matrix.prototype.rotate = function(direction, id, length) {
    var clone = this.state.map((a) => a.slice());
    for (var y = id * direction[0]; y < (direction[0] === 0 ? clone.length : id * direction[0] + 1); y++) {
        for (var x = id * direction[1]; x < (direction[1] === 0 ? clone[y].length : id * direction[1] + 1); x++) {
            this.state
                [(y + length * direction[1]) % clone.length]
                [(x + length * direction[0]) % clone[y].length] = clone[y][x];
        }
    }
};

Matrix.prototype.toString = function() {
    var out = "";
    for (var y = 0; y < this.state.length; y++) {
        for (var x = 0; x < this.state[y].length; x++) {
            out += this.state[y][x] === 1 ? "X" : ".";
        }
        out += "\n";
    }
    return out;
};

describe('rect', function () {
    it('should light up stuff', function () {
        var matrix = new Matrix(3, 3);

        matrix.rect(2, 2);

        expect(matrix.state).to.deep.equal([
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 0],
        ]);
    });
});

describe('rotate', function () {
    it('should move stuff around a column', function () {
        var matrix = new Matrix(3, 3);
        matrix.rect(2, 2);

        matrix.rotate(X, 1, 2);

        expect(matrix.state).to.deep.equal([
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 0],
        ]);
    });
    it('should move stuff around a row', function () {
        var matrix = new Matrix(3, 3);
        matrix.rect(2, 2);

        matrix.rotate(Y, 1, 2);

        expect(matrix.state).to.deep.equal([
            [1, 1, 0],
            [1, 0, 1],
            [0, 0, 0],
        ]);
    });
});

describe('toString', function () {
    it('should show', function () {
        var matrix = new Matrix(3, 3);
        matrix.rect(2, 2);

        expect(matrix.toString()).to.equal(`XX.
XX.
...
`);
    });
});


describe('compute', function () {
    it('works', function () {
        var result = compute(7, 3, `rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
`);

        expect(result).to.equal(`.X..X.X
X.X....
.X.....
`)
    });
});


if (run_for_real) {
    //noinspection SpellCheckingInspection
    console.log("Result is", "\n" + compute(50, 6, `rect 1x1
rotate row y=0 by 5
rect 1x1
rotate row y=0 by 5
rect 1x1
rotate row y=0 by 3
rect 1x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 3
rect 1x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 5
rect 1x1
rotate row y=0 by 5
rect 1x1
rotate row y=0 by 3
rect 1x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 3
rect 2x1
rotate row y=0 by 2
rect 1x2
rotate row y=1 by 5
rotate row y=0 by 3
rect 1x2
rotate column x=30 by 1
rotate column x=25 by 1
rotate column x=10 by 1
rotate row y=1 by 5
rotate row y=0 by 2
rect 1x2
rotate row y=0 by 5
rotate column x=0 by 1
rect 4x1
rotate row y=2 by 18
rotate row y=0 by 5
rotate column x=0 by 1
rect 3x1
rotate row y=2 by 12
rotate row y=0 by 5
rotate column x=0 by 1
rect 4x1
rotate column x=20 by 1
rotate row y=2 by 5
rotate row y=0 by 5
rotate column x=0 by 1
rect 4x1
rotate row y=2 by 15
rotate row y=0 by 15
rotate column x=10 by 1
rotate column x=5 by 1
rotate column x=0 by 1
rect 14x1
rotate column x=37 by 1
rotate column x=23 by 1
rotate column x=7 by 2
rotate row y=3 by 20
rotate row y=0 by 5
rotate column x=0 by 1
rect 4x1
rotate row y=3 by 5
rotate row y=2 by 2
rotate row y=1 by 4
rotate row y=0 by 4
rect 1x4
rotate column x=35 by 3
rotate column x=18 by 3
rotate column x=13 by 3
rotate row y=3 by 5
rotate row y=2 by 3
rotate row y=1 by 1
rotate row y=0 by 1
rect 1x5
rotate row y=4 by 20
rotate row y=3 by 10
rotate row y=2 by 13
rotate row y=0 by 10
rotate column x=5 by 1
rotate column x=3 by 3
rotate column x=2 by 1
rotate column x=1 by 1
rotate column x=0 by 1
rect 9x1
rotate row y=4 by 10
rotate row y=3 by 10
rotate row y=1 by 10
rotate row y=0 by 10
rotate column x=7 by 2
rotate column x=5 by 1
rotate column x=2 by 1
rotate column x=1 by 1
rotate column x=0 by 1
rect 9x1
rotate row y=4 by 20
rotate row y=3 by 12
rotate row y=1 by 15
rotate row y=0 by 10
rotate column x=8 by 2
rotate column x=7 by 1
rotate column x=6 by 2
rotate column x=5 by 1
rotate column x=3 by 1
rotate column x=2 by 1
rotate column x=1 by 1
rotate column x=0 by 1
rect 9x1
rotate column x=46 by 2
rotate column x=43 by 2
rotate column x=24 by 2
rotate column x=14 by 3
rotate row y=5 by 15
rotate row y=4 by 10
rotate row y=3 by 3
rotate row y=2 by 37
rotate row y=1 by 10
rotate row y=0 by 5
rotate column x=0 by 3
rect 3x3
rotate row y=5 by 15
rotate row y=3 by 10
rotate row y=2 by 10
rotate row y=0 by 10
rotate column x=7 by 3
rotate column x=6 by 3
rotate column x=5 by 1
rotate column x=3 by 1
rotate column x=2 by 1
rotate column x=1 by 1
rotate column x=0 by 1
rect 9x1
rotate column x=19 by 1
rotate column x=10 by 3
rotate column x=5 by 4
rotate row y=5 by 5
rotate row y=4 by 5
rotate row y=3 by 40
rotate row y=2 by 35
rotate row y=1 by 15
rotate row y=0 by 30
rotate column x=48 by 4
rotate column x=47 by 3
rotate column x=46 by 3
rotate column x=45 by 1
rotate column x=43 by 1
rotate column x=42 by 5
rotate column x=41 by 5
rotate column x=40 by 1
rotate column x=33 by 2
rotate column x=32 by 3
rotate column x=31 by 2
rotate column x=28 by 1
rotate column x=27 by 5
rotate column x=26 by 5
rotate column x=25 by 1
rotate column x=23 by 5
rotate column x=22 by 5
rotate column x=21 by 5
rotate column x=18 by 5
rotate column x=17 by 5
rotate column x=16 by 5
rotate column x=13 by 5
rotate column x=12 by 5
rotate column x=11 by 5
rotate column x=3 by 1
rotate column x=2 by 5
rotate column x=1 by 5
rotate column x=0 by 1`))
}
