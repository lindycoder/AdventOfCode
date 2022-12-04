use std::collections::HashSet;

pub fn version1(input: Option<String>) -> String {
    let data = input.unwrap_or_else(puzzle_input);

    return data
        .lines()
        .map(|e| get_score(pick_common(split_to_compartements(e))))
        .sum::<u32>()
        .to_string();
}
pub fn version2(input: Option<String>) -> String {
    let data = input.unwrap_or_else(puzzle_input);

    return data
        .split('\n')
        .collect::<Vec<&str>>()
        .chunks(3)
        .map(|trio| {
            get_score(pick_common(
                trio.iter().map(|e| e.chars().into_iter().collect()),
            ))
        })
        .sum::<u32>()
        .to_string();
}

fn split_to_compartements(line: &str) -> Vec<HashSet<char>> {
    let (l, r) = line.split_at(line.len() / 2);
    return [l, r]
        .iter()
        .map(|e| e.chars().into_iter().collect())
        .collect();
}

fn pick_common(sets: impl IntoIterator<Item = HashSet<char>>) -> char {
    return sets
        .into_iter()
        .reduce(|a, b| a.intersection(&b).copied().collect())
        .unwrap()
        .iter()
        .next()
        .unwrap()
        .clone();
}

fn get_score(c: char) -> u32 {
    let ascii = c as u32;
    return if ascii >= 97 {
        ascii - 97 + 1 // Lower case start at 1
    } else {
        ascii - 65 + 27 // Upper case start at 27
    };
}

#[cfg(test)]
mod tests {
    use crate::day03::{get_score, pick_common, split_to_compartements, version1, version2};

    #[test]
    fn example_v1() {
        let input = "vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw";
        let result = version1(Some(input.to_string()));
        assert_eq!(result, "157");
    }

    #[test]
    fn splitting() {
        assert_eq!(
            split_to_compartements("aa"),
            vec![
                vec!['a'].into_iter().collect(),
                vec!['a'].into_iter().collect()
            ]
        );
        assert_eq!(
            split_to_compartements("aBcDeF"),
            vec![
                vec!['a', 'B', 'c'].into_iter().collect(),
                vec!['D', 'e', 'F'].into_iter().collect()
            ]
        );
        assert_eq!(
            split_to_compartements("aaabbb"),
            vec![
                vec!['a'].into_iter().collect(),
                vec!['b'].into_iter().collect()
            ]
        );
    }

    #[test]
    fn common_picking() {
        assert_eq!(
            pick_common([
                vec!['a'].into_iter().collect(),
                vec!['a'].into_iter().collect()
            ]),
            'a'
        );
        assert_eq!(
            pick_common([
                vec!['a', 'b', 'c'].into_iter().collect(),
                vec!['A', 'B', 'c'].into_iter().collect()
            ]),
            'c'
        );
        assert_eq!(
            pick_common([
                vec!['a'].into_iter().collect(),
                vec!['a'].into_iter().collect(),
                vec!['a'].into_iter().collect()
            ]),
            'a'
        );
        assert_eq!(
            pick_common([
                vec!['a', 'b', 'c'].into_iter().collect(),
                vec!['A', 'B', 'c'].into_iter().collect(),
                vec!['D', 'E', 'c'].into_iter().collect()
            ]),
            'c'
        );
    }

    #[test]
    fn scoring() {
        for (i, letter) in ('a'..'z').enumerate() {
            assert_eq!(get_score(letter), i as u32 + 1);
        }
        for (i, letter) in ('A'..'Z').enumerate() {
            assert_eq!(get_score(letter), i as u32 + 27);
        }
    }

    #[test]
    fn example_v2() {
        let input = "vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw";
        let result = version2(Some(input.to_string()));
        assert_eq!(result, "70");
    }
}

pub fn puzzle_input() -> String {
    return String::from(
        "rNZNWvMZZmDDmwqNdZrWTqhJMhhgzggBhzBJBchQzzJJ
pHlSVbVbFHgHBzzhQHqg
nVsqGpbbtDtTNmrmfZ
zrBMnbzBchshsttfbMRBgmJggmmCHGgDhDgNDGHL
VddZqQqdvSQMJHJGdCDCDDmH
pZWWllPQlPZQvZvwpSVlqlvtfswMRzBbntzRbzbfstsRzF
NnjjRlnWNSWWbGwccbcchfPfTvfjfTBBpvmdMjTfvB
FVzJtDDJDqTMlmlM
gVQZlFLlzHhLGShGww
rPZtvtFrFPgWjQvCBlcqMzlqQC
QGVDJJnLnVTCJBczqqTM
fNSSnmLDSVLhhhSNSLhGSGfVPjrFHwmQwtwWFRWRjWPHrwgt
SvmlrVrCvmNhSSVZVCrsgqPfbwGFwwwsflbbGb
QHffdnHDDQdMGbgqPwztdPds
DjBjWHfQDfTQWTBfpMBQLVmmmcCCcVhCBBBhhCmC
trLHFFQHTLHJQrflfCnLLHrRfRRPqSRPbPbbsRGqqGqhjj
mcMpNWVVNmNVsSbSJPcGhPRR
NpzNgwzZDVNZVWNpHJQLQHtQrZQHrBCl
JVCMfgJVrJtMBhhrfVVfhVsjvpFGFgjSSgFdSGGqjvjvqF
mHllHlHpmWlDSFqbdSTS
nmZRLzQnWVpctMVpQs
BrvRzWBPWbRwGRjbbRGrtrfqjCJCjCJgJsZJscFCZcJC
MnnnVMVhTMQhsccVfwqFJgqf
mMShHHppQmHrrBzwtSbWwR
pWWGJMJJwlnZSqjWmvSWZC
gtHrLttDtgFjjqRZZCrjpp
bFtbTpHFHLbfLFbHVttccttddJGQdJzTwdTzJlMnMBwwJJ
JhqHFhVMzJPQcdcVncdc
NhgfwSjwCWwltSfnrnRWZdpcPrrRnp
NNhlltBjssNBgwLFFvDmDqLzHqBB
LnFrnddfrLnMFjWzpFhcWpjpFc
ntCwgtNggCqCgCqqPPltvcjjhvmWhmvDzTzDzD
lqlVQgVCSPVllVQSNGMHHrdQsHrJJBnMHHJf
ZGZcRZNWpcHZhJfbbNblrfrgllNr
stBMtzCCsHMfFQjfSSPgtt
qmszdsCzMncdGwdWZGvH
PccqPqbhvSvvvtWNjTtWsWcscp
gRwdDzHJQgHzfdRhgHRffzwsTTjTTCjNjssCpmWWDjtCLW
zdRMwdRHhGJwgHlnGGSFvvSrnSrr
rRpMJtPwrcCTNNQNMZQm
mDWdWVddbbbmBflFhvTHjjQjfZTgZgLLfH
bhBbFFnDVhdddFBhdmpJRrzStJmwnPzcsJ
RjlpRRWzzRGRmGzlCRRlQjCgtvTJTtJrTPttrWTwhFvvVJFT
bSBdLLqbcqcLndLHZNqcZdBDPrVTDDTJSFrJJvVthTwwDS
cqVsnBfHffVdqnZccGMmCsGzQmjsjlljgz
wMzJhLtwbnMWtHcFCCFqFNNbgq
fMlMfjrRRmdmGCGVVCHcVqcVTC
MmRRRlvmQWzpvnZpwJ
gRmgMRMmRwzzmwHbwcTNqPDVBbPTZVqPNZ
fWHphpGFpfJrrhPsNTNZVsNVhT
WGfJdvltJJfHrJpRgvMRMSwRznwMmw
htJFGsGspCppCFCGthCdpmJmgmWZfqqzWzlWcfgZHgzHlg
nwVMjVcVcWlbnBlfWB
wcNDTvPPDMFJLLppDGDD
hjCBgPbvMvmQDzlWnWjm
HrHtgZRRRNwczDWwwDzsQQWW
LpTqNtFtLFqHLHRrqgFHffVVBChvhhVPBCPhbPbp
CwpbCwjGqSjVllpGCllBfhZZRDPNcPPNvLLLDSDN
WshFFWsgTHsdMzQvPczLfLZDZRcLfR
rWsJQTMhWWHdsQTgsFJgllClVpqVbqnGblCppCVr
gRBSGcBDBSJSvPQwrTFLjggQTQ
HMMnHHHZfFVFrrMT
HhlhppCNcJzCTtBT
CCffCCmRLTsQRPHQQMPF
dWdbgcDSNclbbdwdSqHsvHPQPTPJplPMFMGJ
DWbDNcqZDSWSccNTVBCzVVfmBVZnVz
BnsrrvZwBsBSJrrrqSTgJQjCbCjgbCHDJgJFjQ
hLmGlnLmGWcjGDgfFFjQdF
hhWPmhPtczWpNRmppzRhLchMsnwZvTMZvVSwwrsNwSsBvr
tDCCltNVttJhNGlMPSWdqBqSjM
RFQcpcRTpFcnFzdLmLSWjMSSBLSQ
jwzzczpFbwnHcDCsthDJJsNbst
dLRWTHSwTmTwTcTWvQNVVQCvVvNFps
GnBPtBMJBPrjGGJMjrlqChNpNlsnhVFhQsVQ
JtMtGJfrJgDJjPjRTZLdFcRZRmwSDH
VSccPJSBLgZPDLDQ
zfpLMmLsHQGqgQHnDD
zdLLMssmrdfhddcVdJtScB
VvpTVQHSqSHSHqqHJVmRJVHpgDBwDgjcDDDgZjBZBjwBZbRw
PCdssGlstdWslFPfNPrtClGjwBgBJgJNwcjBjBgZwwMBJD
tlJldhdhdsdhTqSTqVQqQq
VGqTcTqbpPwrjfbl
BvntnZNNsLZvLszSnCsvJthlfjTrZwlrjrpPlwlhfwrl
QBtNtJLvTsFdQcqWmQRR
fjcjhmjBvcvcSvcZ
HMwZtRQQpGGRgzMvLnWWnbLlSntlbv
JQPzzJHqQRqGMMQwHwzDZZhmmPfjDjmjsCZhPj
cBlZZMfBrCBMwBMCvQzTwFbQzPnbwjTbTg
WtzpVDzmtthzGFQTbTThnnTQQg
sGWstpHdpGDmdHdmGmmmJNstRMrCcBSfBSzNBNRrSRNMcMMv
mMPDVBZZLSmRdcFpjr
fggGGfbfgQStjjsdbtdt
gNqQgCQlNCCJgJHvnvnHMjPHjv
bLsRQrQsGQbLrbRZMGgbJJBJFtlFFngJphhcfBBq
jjdHCCjfVNmmmNDFcBcpBthcplFDFq
jmvvmWVjjHTCVvNjSbQGLrRzwMWsMRwfGG
sJNCsCFFCNPhCzlrSvRrvwhRjj
MMGMTwpMHGzrGczzlG
qVmwgHtDtmCdWCsNFmNJ
fmhWhjVjNpqRRJjwRw
gnGQGDDCgSsCvPlvPgnPgnPtwqbpHRHqHdJpzpQJJJRJRF
wgPGsDGPsZgGgBmBWNZNfLWWrZ
WdsCVtjWWWHRRqLLHncC
fbSpMSPSZHRRcqlpRc
cGMmJmfMPPPccZMNQPWvjTtdTjvgmdtTsggw
tPBQhHWBtQHgWQCtLwddcGnfpGpwwnbhVb
vqQzTNJJJTvRrTNFJsZrrzFlbbfcnVbbcwmGGGpVzmddcdfd
NSSqJvFFFFFQjQCjQDSDPD
rQZnVVrZmZmgSWqHrSzHPC
LGFLwcMBcllBjFNwGjltggSqSWCCzvNgSqSHtt
wdhqqGBwwqGMcDhcwdFFbbJppZbssbfZQsQsdVQm
lqBZlsjVTbVqmFrSnTFSvwncPP
zQztHfZQtWLJzPFnnQScFcFrvS
ftHJWHhfttHWffhtgLNfZDWbdqBqjbVssBDCqCdCsmClGG
MlbWFTJQFbFFzRdNjNtjdtBT
srwnrsLVHzQPQsjjSQ
gLpnwgnwnHCvcHHcvwgCvGFFhWGmFmqMMbQFQFFhlGmJ
qqNcJgJccdqhsqgsggdgqgcrtfNWNZzVbvVFzttMfzbVMZ
GLlpPpCpwPLDGvrFVWrWWbZt
DlRCDDLSjTjDjSRSjPClwnwSHHHQmmQvTJcQgvddHsqdcgmB
jmRjRbRQLLZbPnbrcTTHHHNn
MfhhmmwtvStrpnJJHc
fgqlvfhvFzMwqfvMfFWlmMvLZsdQsZVdCdLZdGQjRzdQjD
lTPcDlVdTlVVMSDfTJccVzdlmMgGBmppgBmnHGHqHqQqqQMH
ZRjWFPsLNLLrPhWNtnBBvnpGpHGpQmHnmR
CtwssCNLrsZWjrjcbfPzwJJJffDbTl
cjMvvqpJFqhShNCRQR
ldtDgQZDPdzztLZgPTtfbnStfBSbNNSbnbhhSS
TDsrzsZZZTFHmVHjcsQW
BQmQchrmBddcmZZdpSgrpswWWswVsnnnDJVnnZFnGN
TfStMPLTHvbvRVGnHGsNnJWFNV
qtvMRMMPbbPMLqRPvRTRzMjSSmprpQdBchlmmgldgjzm
nRRnvNPhrbZDLjvS
HCszMwcHHcLDrbQDWr
ptszqwdMbnnhPBqN
QbzhhfbFhBbpbzwwLjLJjSjltL
mNndGrSStHJTJLln
rDMMNVWdVpCbSbSp
tDTSTSTTTTJDwqjWqBWttdjg
nNPmVfnGfPNVLmNzfnzPVFMjdpBwWZwZHwBLBqgjqpWH
dfGPfVQGVPhGzlmnzSvsSTDJhTbTTrrSRD
ZfgtZBptBfRQNQggjjrjjwmwsQJPzrwm
TwTGGwTwzzsJzTsH
lFvwqFLhFMnqcLlVLMLfptNWppppDBDbDfbFgW
mjftBfVPjttmjcSjcPttzJlvnrwvTRrTnvwvlRrHHTHRTR
WZDWDNLFWbZbcMDWGZDbNdMCRsnTdTvdnqrHCTrvsRRvwC
DQFZLNNgtBJQcBzJ
HbZQZFVbQVpQplQZGbGchDffltfLtmdgDjggTmtm
zWzRCdnCRBRdJrzDjLhDthjLJTTtjq
CPPnwSrRdRSzCGMcZZZMwFwMZF
WBQqNQnQllwnWQlvBBMlljHTqqFdGfmTdFfcFTFFcqmP
rsRRVrZhrzbtpZRRhFDmPvfFFrfTdFHGvc
VtSCtSLbtsZVtttthCbJSWSlJlwJQggWWglvwW
QfFLWCvRfSLFCtvtFhNcqDDcGVbhGcqh
ZVgrdZZPPZZzPwdjzZhmccsqJGqDdsDDNddD
pzzwpgZzZZTznZnjZZzPVRLQLlvfSlQRSpWlCvtSQv
RtcHhRMcrHhBrrTNDVBNLqLqQqfBPm
wCbWzWbvdWCjbWppmtmNmqmLLsfsNV
lwjWdbztgHTgggnnnR
flBbzbMfbrTlrMvBCcwPggdmcdmg
VDVVRFZRZSFFhQLSGFQhjSVZCgpvPwLCzpdWWzccwdvvvwcC
hDHRGQVHHQVRZSQGbqqfNTlbHzrbbsqb
MTFdTsZpPTcMpFCPdCBmMBmRfRGBmQgQRRgt
vbDSwvhzznnbbhDWnvSzRBgQQLgLQltqtqlmwfGB
jVjhfSnNDNbzzWzjWSjrCFNpcHdpTTJddJFpsJcc
ZrrZPHfChPdDPVVdDq
vFmsbTsmSbbBJssmSBvTmmnTrnrwlWqwVlLrVTLLTWqL
JrFbpsvFBMBmzBzFStcRhjZjfCCpZNCtct
TGgRrTggwwtvtQtdCdQNqN
sJHZJVZHDBpFBZBBNzNdhzdpSzddvqhN
VZcvFsJVFvsmvssbcnrwbrnGMbMlRn
SdcdWzMJdSMWMddZJdVcmBmwrwqrrnVnVNtr
mlQHCfgbjsfQTbfCBNtVhVnntVBnVh
HLDslDDmblgHfvLHPJFSZPpDFpFFpdPS
qNqPNJvcSzGGPQnGQp
bWhbgsshZWBhltthhbWtCsZNjrzpnQnnznnjtQFrjGjVFGnn
bRDNddhNdDsZdNChmvDmmwqqvLqwSJDq
TnSfPnCSmnSgpSTmfLzfMFLWFJJLWWsBsr
jdQjcdqDVVwDcPsPzMRJMLqPqR
PGhGchjhtZlTGTHCCb
ZZRrJJqSqJwNFFphsGsLPJ
blcMCflvTTPFFNpVvsFv
CcTlltTmtmMdmCmnlllBDDSDQSwSjRDQSdswjR
MCCPNsnQFWbvvTPF
CcCVJJhjVJZRtcCclDDlbcbTcGFFDz
HpjtVwVZfpjJVhZgCVtLmrBwdMrLsNNsMmdLqB
TJTDTnrFzzdWgWGJSSMJwg
LhPVttjtLmsPqqqVsVpsjLlgWlwHvGnlHWlgHlGgwvlP
mQshLhmsnsqZcqhZqpshsLVpNTNbBfzTRBQdFRzNNFBTdbzR
ZGqMLGqvJsJsMJmd
PDVQPfPcrrcFrrzrTdgCjSSCzgszmlJjBj
PfRtVfttVcWtVJrfbGqvwqLpRRwvpppH
HmLmMSnnWnrTrnvpqFCHVGfzVFVHQj
ttsstRhhcNwbswNtdwsdNPFfjzQppQPjfGGfQVPCpR
bbsDNtDcbhstsSZLDmSSgCmnSS
tfwBBLcJVrDnqvLv
zmWWJRZhWRRRGRNdgSZGgWTvpnjvrDqvpHjjzrpnrPDnHj
NdJmSGZWRhRNsghWTJmdGfQCtllCcFMwffBftsfMQc
lTLgTghpGZJDBrnGWnnm
VlRwlHttwqmHHbDWHJ
twldzCvsRdsFFtRtSczTjSgMcfSpSzTM
pBpMBTcSlNtMcTfFCmbPDzCDLb
JgrjjJqhGZQrQrZhnJGDDCZfvPDdDzFFdzfmZL
QHhqqnrVJJPhHrnGQgwMNwMMctcWRWSBMNtNsW
FJrlhpcfDCcFWpNpwWwjNQwz
RTTvPdbjWzMbnNNM
GRZTGggGgtvjGcqrBcttcDlFhr
pMRVdVbbMMMSdWWqHpCTvTjnBBBFFGGB
smNfZgcsNrcmzggZszsgRnPGFHjBPTBTjGjPTBNj
RmwgsmgfrzzsZtfgZLQQSVWlwbdMhlwdqQ
mRRjPmLrrSmzSczSzPgVZFpTCpZCMWrZQMQrZJZT
BvdbHNdnJtvBDbqqdBlvwvqpDQMpZQFMCsQCspZTMMCZCF
nBlfbfbndJBHPfLRfmhhhhPL
ScJDFBNLLbVRqVfZ
rWrgmdMgnnBhBtnntf
CwBWWMgCwddCgwsQjsrvNvlTJzSNHwNTHFJHzS
vnddCrNpCgtjLdSdgCgCCvLnWqDhWBQhHqQHDqBhQHDHNNDl
wPTVfVTJmZGJVJGffZBwHMWlWlHlWtbQDqbl
mGsJVVJsTVTTmtJVzzTJjdSjjprzCvpSLSCjdnLg
zLNggsVHmNNsssLmwzLQZLwDRvGQBqGGDDBBvvDBDqPhRG
WrCjbtJdbFhBRglGgjqv
JWCJcWcSdWcctnJCcJJJbcbmzwwznmgLzNzmLHmHZMwsZL
JRRDNNhhszMTzNMwCG
MnHPqmgmHjPnnvjqdmjFLQwLwTLwzTwTdGLCzS
BnPPZqmcfqgqnnZmBmqjqhfWVJlRMlhWlRDlVsssbh
nmTLTqsvqnwqsvwDPnLHdNVrMMHHCBlmVdmGNV
RgRpcJhQRfQZcJbWhQpBHCjVCdjCVGdddMllHp
fczbZhzbtcZfgRRBcWSPPwFsLSDswSwTsSzw
rbFpzFCVBrrBZCjbCzHHBVdJllGDLsLrDtsswswstGJs
QNhNNnNnnQhNWSnRhnJtdpJpJtMDGsGLLtsQ
ScmRvNRNnWWvNvNvfpTccjVZbqgZgVzqHjCjTVTVVq
BTppwCwBpwwBqnjlHcLBTHnbbSbDthsSSJgsnDDRgJRD
FVGzzvrdMGSSsdtZtZgd
QvQtvtGFlBLLjLQL
gsWWsNMjwgPMPWnMjShHHZSZbmZbbmTSnb
rlCvVQrCfqffpVjQRqCCvDDTTTmmZhZTmZhThFmhhZZhqb
CDDVJpVfrJJVJLMNzMwWwLwj
nHrcsZrssPcBPtQJLJtQQCZQpV
GFWzNzNFdNbTMMqbGTqTqzqqdLCpfDQCtRVVCLtdCfQsdCCt
TlNqGTWFNmMMszhGsmFTWGFzwHnvSjgPgvgSjllBvBnvwPBB
mpMggjgMlmtjtGMwZpcSscBlcsSblhsfSdfs
zzPVDRrLrCTQNCzNRTVFNLhBhBSqdQbcfSsJBJdbjJfB
RPTRPTVNTFzVrHVDCrTHmHtwMvwWMmtwmGjWgvGv
rLMcvfHVfMgLFvfNnBBzwRbBwnrGNs
dttJjJCtdjmwzwBCRRCqcs
TddDQDJDtQJtcJFpPQHPQMvfQlFL
LQSqqpqTCSJcsDcqQMMhnnjMjppZhwHZbZ
NRtvtmgmvdBffgtVCBWVRgFbPzHbMHbnwwjMPZfHbPjzPP
RNtvCvNdgtNNmldgvCFRNVLsQLqJcQGJJrccGSlDLDLr
GdwwqqqwGVtjdPvTCplbHTPbPzPTpp
RpLmLLpFfNsgTzclhzClThgH
ZFsWZLFZJsNsnWsnRsRfnfJQGBttjdGJjBvvwjdpjjttvj
tfPzzLrrdrQlTlvn
qJRBhNhNGVRBFRTlnJvCmvmJPCCl
VVPDNchNMVFGRMFcRVBjsZZcttSLSZzzStcWtZ
pTrwTrnjtttjprTSTNTQfcjcgPsPZfPgjdgdsQ
mCmCzvzhmJDHzJDbhFCDPsgddcsfcdsbdgVRpdVs
zqJzFCDhmqvGhMmCvmGhMCGJnSlnllSBLllLMtNpWtpNBnlt
JBhJrFLhGrnJZrlcbffndnggfggf
jqmWMGGSsqCsmpjmsDQzlcHgbtdzjjlVfctjHV
GWSmSCspCsMSpRmSmqMMCBvFLJLhTTwFhRFLLBTwrv
BCdWccqcqpQqrsNgGsWMgfNW
lFttLzzLwnfsLrsNsNLG
zjNlznlwvRPZnltwvPFnZRCbmjCcqjpcpQcqVVdbdVBm
CwTbbCGNFHtHwwjSjJpzjLMdMMzT
rscqqVvWgWrZMjrlmSzzmLrM
WPqqZnPqgncnBQQVRbCDwRHGSFHPwRNw
ZQnZwWjFvdsHwBJltfmfSlsqlJ
gPprhMDTpMpPMVNqNRqNlJhltJdJ
pLGCcCrgppCrVcMpdzjvzvjLwQQzFjwzHF
NmmmvfqcvmLSQhCLvtvL
TVlWTZVJZJsFbwWbQQhtQgLFCnSgghLt
hZJTJZhwZlRJrJWHVlblMBffmqfdNMjdGdBBqqcH
GJJfLfptGqqqnsVqVVjjDnNc
mZPSvPmBCdmwdCLDshSbRnnDDhRL
gvBrBvPBPPZCTLZmwmrgQdwfTJMHGzHfWffJzFzttHWFzW
sBMvmzWzmFmNWJfffZNLfbqZbtZq
jRQVRnhhppnVhjgnDLttLqbLqLQfDLss
jRRgpGVGhwhnspgpRppwSnBvMMcWvGczGJJHdmHJmJFF
VCLHFwHMhLghHHWhFFgWNMMVzmdmbvWdJqBPJPPBppqmBdzm
SRTsjGZTsZZnSnGZGqdBmrqPvmqqqsPpmv
GvQSGtZSQllVhtLMcLLNMH
GsNdWpdVWGSHjFCWCqFFgqngvW
mRQTcrLRmZTPRLPZfqqqHbDDDgFvFnvqzQ
hfZHrwwmcZRwlLfwlmrRjMJJsVjslVNBGNjpVBBG
pllpztRqBBvvGPpG
QQhhZQbVcZQTPMWWGbvvbMHM
cwgCQCLZChQwwLZVzCrzzqNCzrDqdFPF
bgcLPvvpcbdsbpSsHRTCqsRfWfsHRm
lZlQtthrnlVMmTHqqqqHSChB
rDtlzttnlSNrMtQjZVrcgGDLLddcdcpPgPGJJd
jvGbvLLQDSGlRmmSLjlDmRQggFBrMCwWdsBFWBFjdrrWrr
PpTfcPZpNTVNpHzTzzzpPJhBcwrrhFsrMdFcMCBFhgMF
JTTqdtfzfzJpqffNdTTHGtQRnmDQGGLQQlQRbblD
CQQCshCMwgQhMdjWJFBPpbjgmmWj
SNNvcGNSZSTDtGDcczJJBmzbjBJjmppbppms
cDtfDVNTGGGNNrwLLwHdqLhfLs
ngghZCChzhNjjNbbJfdh
slPPRLlBBlVRMvRllLLHvcpcdFfJjvdFpfHfcZ
RDZPZBLmPVWDVrQtnzSTmgTwmTSg",
    );
}
