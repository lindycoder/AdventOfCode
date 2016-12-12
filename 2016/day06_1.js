var expect = require('chai').expect;

var run_for_real = typeof describe === "undefined";
if (run_for_real) describe = function() {};


function compute(data) {
    var sets = readData(data);

    return sets.map(highestOccurence).join("");
}


function highestOccurence(arr) {
    var mapping = {},
        letters = [];

    arr.forEach((e) => mapping[e] = (mapping[e] || 0) + + 1);

    for(var key in mapping) {
        letters.push(key);
    }

    return letters.sort((a, b) => mapping[b] - mapping[a])[0];
}

function readData(data) {
    var lines = data.split("\n"),
        result = [];

    for (var i = 0; i < lines[0].length; i++) {
        result[i] = [];
    }

    return lines.reduce(function(result, new_line) {
       for (var i = 0; i < new_line.length; i++) {
           result[i].push(new_line[i]);
       }
       return result;
    }, result);
}


describe('lowestOccurence', function () {
    it('should return the highest occurence', function () {
        expect(highestOccurence(["a", "b", "a"])).to.equal("a");
        expect(highestOccurence(["c", "d", "d"])).to.equal("d");
    });
});

describe('readData', function () {
    it('read_by_columns', function () {
        var result = readData(`ab
cd
`);

        expect(result).to.deep.equal([
            ["a", "c"],
            ["b", "d"]
        ])
    });
});

describe('Compute', function () {
    it('should do stuff', function () {
        var result = compute(`eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
`);

        expect(result).to.equal("easter")
    });
});


if (run_for_real) {
    console.log("Result is", compute(`blrqqadw
hxwteava
xtzzneor
ufydaiyx
hhvcoozu
nbbvuvmd
usvdcalw
rpntrbyo
kgjholvo
nlohafzu
gxmifiuy
xndolmhm
zmtsfmtq
wkdzmogx
aogqflji
uphmjtnl
jkqognlw
mdzsbrij
zyxolasw
kvdyikgy
xpxgmuqq
viuoqyap
simgbmca
qxcjewnz
ivwoedjr
mlmzozlr
jmyallmm
oeecmjte
miuvzeww
qtfsiigb
lstgpdfp
pevoamxy
mjtpbedv
ugbasbgg
idcnuhtx
wwhcrxdr
prrugmrq
npoiywvw
zpkohigv
wngoczfk
gxnmxano
cbacsmte
meclajtf
zhztflqy
grqqlecu
qjbzsptn
ebagoidi
egegrnyh
jccwkqle
ikkwrzqt
nedkjwhf
vildwwrp
ugrejotn
kdajfbqw
gyiwhxpd
eemhkuwh
jvfhoiqi
wsgyaiip
jzjvagvv
lqupczes
fetfptqt
msmlbgcf
iukfpgrm
ctymfjpj
rbrpmkvx
glooxgap
scctgiai
lakkjuyk
gaekimfl
bhfaybki
qaiazzpf
dwqkvsee
fuhbygkt
zhkggelc
haigokzn
jpuangaj
tpunltos
izqxnhhd
oeyxnqkn
vzvelmik
ddnaozap
mdlhkdlu
oglyexnm
mcgxswpe
jzkjknxc
gfqnuhfs
ztnxzwng
bnuxixlk
vmumdwec
kuxxbcbv
vdcfhyso
qtdesxqr
qciljohn
qqlluqzz
njhvvqbw
knakngrj
pradgsbt
koffjwwy
tvrkgjql
mqtxerte
smigupym
bxxvoskx
jerbindg
snlgnowp
qsuxtdsu
fnpexyoa
ffwifdad
mvgrpczm
oxszzrsb
pxefzlch
mcgbeauh
neseoapm
iwnulsrv
zhinoifi
lfmjmmtk
fsxcqurn
gmkkhfuh
nuqeimxo
uvjdgkdo
ohtmvkcu
albuiptc
piaihrgr
fjviblws
qotlvddl
gchijkjr
azzrnqhy
xrynrbck
pdvkcekk
thscvzai
eoapfznw
hpgoissz
ifnesaoy
eniqycje
hmjmghcp
sfyrvbbi
tuxcoidt
icysmkcf
ycagvtls
dohqfcgc
taitvkzk
bblnroyh
grdklrua
qpijbooa
pcwtjacj
mrvxbefl
oodwrtvj
xosqbcie
zbquakff
ypwpamng
rpfbkssq
fctgmcav
hdtcdfcf
ctboapkz
qypakerm
vebdtsmq
cyxqtbtt
dcnpkmnu
hnjppwfo
gqmfdahb
hxiqcrbe
rpxazkak
nmtraoky
sisqtogo
oycwooev
lmmitjey
rytzptco
waatgjdu
khsuxyse
cxjltfxn
eedsmcld
fngdicwe
lkomchdq
ulvabpoz
oyhjvimr
dpyexiwi
wjfzkbbv
ihohnaxx
ajxfefrv
bplrrpcz
rtamodoq
slwrcibk
sgwdtumz
vlemhplz
dnpkqvad
ytolejsa
ojevrxsc
bgbmnvyv
lmrousup
yyubvohm
bqaqltmt
vfbzzthz
ylehjmop
exddqqwo
xqfxejzq
myyuypku
zyvmvbla
cnpquvbp
yaxdddeq
cnrjqdra
lwphgfgf
zqdbcnmn
qelivdwx
wpnwomgu
xzephbpa
yghrabgr
pnjsyhth
okdznczw
urwcwwfm
hjrsrrzk
foklmzqs
mjldwaun
dabalbmb
jmtqvwst
uhtzixah
blclhmjf
wilsnjwb
qeeriszr
vbfagerv
afegxkkh
zwzausdd
ysfgzvbw
ymjlmnmz
rnrbxnij
ihvhqtvk
ofwrugbp
ontvlhfu
sfjgpqpx
oyzkaiyl
xfmvkfkh
pqpeeptl
jdyueahx
plghatyl
yrdizope
lrurgkqw
xdqtlmww
dkaiotxb
iegjcmln
iupoupxa
zrepcilx
tpewzoxi
munsmbpj
fvhsucvb
rlwchfml
kcmlbubj
jnhurapr
dflwxeii
wtypbujm
jivypmpr
argvlhnz
acyvvplf
naqafzfw
ngepfsju
xfpuwtji
pqgkxbmj
oeygjbxs
evoydkqq
nhuoohdi
wrznguek
ssirmkbq
ackhglvh
egszqozo
rhnhhxul
mqabqvun
yunlcuvd
zklsneau
itanrdqb
pvxbkwoc
rqbqjyuv
ioxjpvqd
pzkgsdej
yklripsi
iohazhoh
umxxpdaw
czfnfgxt
xaxvkjjc
qhgvdvaa
iobwhxjq
jwfwqqjs
cbrfgjpp
conpdlzv
wbcmssue
gyqkseid
ozrzahxt
rzowboce
lhntmyie
tlrcktzc
lxmzpvku
ckliqrdt
qlmalosg
ovvyxrnr
gctjwzrl
ooqvxzac
dbdqzzly
fpsjzuxx
njndzgel
hjfqofhh
txhcpktf
otceqnmc
dduyepiz
bsxdbzgs
zklbicun
rstnuwtg
tasiqsbs
wewnwuyn
zvgkuxxp
nxcmlrmx
mizqhlnv
xyxzfeca
qkeuwzgi
ajnzmfks
ejszlxyc
xzfggxpd
jbooydts
eisoqvuo
hdfpevns
alybbyrb
yvpylcnz
tdpcycrv
kwptuqyw
ncobyufk
fclvkbek
tgnfcfup
vbcuaudl
hublkdvy
aoetzcyl
fsiuwhbi
eyolgmxh
siptvnjn
shvycepr
ntrwmime
dbdnbfyt
bwluchce
uigenqhy
krxdyhap
avycqglh
gguniqpm
wcwzelyd
wzurdris
rmhstxuj
vuaozvvq
bsdgqrpx
twnvkunt
nqgqtugs
vzkvghwg
ypceflob
dsyzunmb
kvhacqqr
ozlfwkjl
pyznytxd
ykdkbfgf
eajwdyia
bhkxsxcc
vytpdoop
ibpypdrh
dkkjnwng
lxwkkldf
nbtckkoy
qtjyffvl
sbitpceb
sxmhbcuy
zorovlxd
bazreact
cwzggemu
uowhquji
eijszbmy
aarneovu
grhvjqyo
fzheiyvq
nzsdrlli
wfsdwsok
wrqjuygq
ggpffnri
wkycrfjm
drksyjxn
smuhwcxa
iabdvvyj
esidunjn
decnfzwl
ysihdzkf
zokmsjgk
pxuddjdo
uemyoegc
glqycmsw
fvfkqzdu
mhotjpqc
pfyuopbx
tibutsqb
krzcqnkv
djqpmsmb
vbufrshp
mmzsrikm
zkjbrtoo
uopielbd
jmketnly
raomwphg
uwocphkf
lvktwagm
lqmorzgf
rihrgrdp
cnbuplfg
hwfjvxcj
sfgptuic
ixkimxsx
kfpicnix
tvpybbrf
navehxpr
rwbcttbq
obqcxwjd
fuiskmfg
xcvfxoeh
tsmaaoyx
qjhiyeex
qwfxiyxq
ctkyxatm
hyxhsvmy
puknicfi
hbwzmyks
uczqlycu
wkywzgqs
kzfehffd
aoooehdc
lnijvgrg
aedbnxzk
lusvnger
ltpbpgiq
aypxjgwo
lgejygmw
auqexwja
fwszagnq
aiafpduf
lyltmest
agtasqwl
fqrlliiw
udarpyjv
kxotyded
aodevwdt
lmmfarbx
snjwogeo
ehfmpymn
yahfaxeo
xudbdnog
rrkxhhsy
hdxadfck
dmnujkng
cujvjtry
srwxylvi
dwohbywb
cvspfupf
czvvjhfw
wvyjwtzz
vfooqywj
bmulxlpz
hbukjylo
bdhsvgdg
vnrrqyue
hjveswxf
yxgzdjwn
byonsarh
edbmtqyz
owvunnfp
wfqqsuyj
cwckbkwt
plesmdky
pzatdacm
nqfyxhij
jjwqitsc
tejffykk
yllyznoo
kkqhuqlc
hxchsqos
buvmceha
kbzymzrl
kiemcigv
txmjfujf
vfnystic
kvaiybnq
ztrwxszz
wiyawlfm
sgedycpx
isafnieb
bpspuqvx
fqjtxrtb
bgjdrvhb
mnsbgbhe
jpsqcfzz
fpumugea
qqutezwg
eoabntsw
tupqchzt
ezwjasja
rsguwrqg
cqzcijqd
rhxlhksr
vcwlknrc
eiqbcafb
lwzbrrtr
aomiovcj
ujxshcar
fbpjehma
bgdphfwg
iukvlxvq
ptawvjzy
styyqrqd
itobtfvm
yqnpsyha
vkwfaykp
zwpoxkzx
uqwasoht
tkgfmnvj
xkilydvt
xlmkpdaz
xfvukjte
yyzpwped
xzxwnrlm
ausmhunn
qgiiljhq
njqhxprl
fgfxiphp
kkzjpuur
dcqixesl
tthldwgg
nkjxnttn
cjtiiltj
drlzddsv
xxluiael
kjjsewia
danhtpxa
edexzcqw
mrqewvuh
opwtwbbt
rdbsaeke
viistwnj
llcndvsm
jeejjqyb
hstekias
gmswtskg
qhdktszo
ptbryiff
jrtlgbag
gjbbbfnu
uirwdwzh
esmntxej
vdcmrenk
tagtsvaz
hnewrron
zydwkvuh
zscfhzxk
sazgunom
gqcxdowc
twmxtniu
wfblhfiv
barpdrob
jwjrnqhv
xvnysjvz
jvsftvqs
jivuhphv
grbezkpe
xuolyqis
smuxlqpu
rticwcrh
huzyzxul
pgqawldg
mdcgejab
rlrgwpfo
uqhvyglu
csinjsjy
ydorfrud
gmcnjnbr
qzvizjbt
vejkuvii
uhfrombz
clgrjlys
`))
}