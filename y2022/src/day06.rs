use std::collections::HashSet;

pub fn version1(input: Option<String>) -> String {
    let data = input.unwrap_or_else(puzzle_input);

    let signal: Vec<char> = data.chars().collect();

    packet_start(signal, 4).unwrap().to_string()
}
pub fn version2(input: Option<String>) -> String {
    let data = input.unwrap_or_else(puzzle_input);
    let signal: Vec<char> = data.chars().collect();

    packet_start(signal, 14).unwrap().to_string()
}

fn packet_start(signal: Vec<char>, marker_size: usize) -> Option<usize> {
    for (i, _) in signal.iter().take(signal.len() - marker_size).enumerate() {
        let sliced = &signal[i..(i + marker_size)];
        if sliced.iter().collect::<HashSet<&char>>().len() == marker_size {
            return Some(i + marker_size);
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use crate::day06::{version1, version2};

    #[test]
    fn example_v1() {
        assert_eq!(
            version1(Some("bvwbjplbgvbhsrlpgdmjqwftvncz".to_string())),
            "5"
        );
        assert_eq!(
            version1(Some("nppdvjthqldpwncqszvftbrmjlhg".to_string())),
            "6"
        );
        assert_eq!(
            version1(Some("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg".to_string())),
            "10"
        );
        assert_eq!(
            version1(Some("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw".to_string())),
            "11"
        );
    }

    #[test]
    fn example_v2() {
        assert_eq!(
            version2(Some("mjqjpqmgbljsphdztnvjfqwrcgsmlb".to_string())),
            "19"
        );
        assert_eq!(
            version2(Some("bvwbjplbgvbhsrlpgdmjqwftvncz".to_string())),
            "23"
        );
        assert_eq!(
            version2(Some("nppdvjthqldpwncqszvftbrmjlhg".to_string())),
            "23"
        );
        assert_eq!(
            version2(Some("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg".to_string())),
            "29"
        );
        assert_eq!(
            version2(Some("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw".to_string())),
            "26"
        );
    }
}

pub fn puzzle_input() -> String {
    String::from("cbhbmmqnmmqvqfqgqcqmmtvvvdsvscvssmfmhfmhhgdgcclhlnnvmnvmnnwngnqggqlqhhbqbfbvffcpfcfpcpmcppsgssvcvmmdwmwsmwswnwvnvvtgvgfgqqnlltgllpplhpllrnrwrtrzrlrzllpnlpnplnlwnnzfztzcchczctcbbpwpbbfhhqllgrllnnghnnlnznzzlqqmggqbgbjjlnlnjllwlnwnjnbjnnhhcddgmdmqmllfjllddmgmpggtvvqqwmmhcmmjpjdpdqqnhhqbhhscstsvttbwtwdtwwjffvccrwrvvnqqtwwhgwhwthwthhvshsfsjstshthqqdfdhdqhqrqggfffvhffhbbwtbtvtwvvwgvvjjjvtjvvlmlmtmztmthmhttjwwmqqjffhvhqvvrddbsbfbgffmcfffqqfzzgmggzvggbjjmccftcftfnttqqjzjdzdrrgvgsgvvlqvlqqlplnnjccjqcjcgjgfjgjlgjjzhhjbbbfdbfddgccncppsbbjjsttcqtqgqpqllqggtsthhtvvtrttbthtnhhddvnnbggmtggcsgcscmmvmllttjbjggbzbttrfttgsstwtftdthdththbttcggdldtdlttbvvpgpjpwpwvwcwjwsjsttznztzftzzjpzzrtzrztrrtsrrdtrdtdbdhhdgdwwnjnnvjvsjjrwjjvrrzvrvllrgghgbbgbsssslqlrllbjbttzfztzpzzvtvccszsddtqttjllqgqgpqphptpwttwtmtltljjfnnzwzmzlzssghssqhhphbhfftwwqmwmzzqtzqzqrrndrrmrqrzrszzrcrbccglgcgwgrgdggtvtpptgtfgflglgrrnvrvhrrhlrhhfchfhdhzzwggvbbgfgrrpdrdccfllqflfmlfmlmbbhnbbsblbzbgbqqjppcddcvvsddjfjjlnnwbbflfzzmlmddjssjffcqffwdfdqqphpnhppbttjfjzzdvdjvvddnfffmjfmfmpfmmmdlmlrrhqqcpcmclmmbmppzczjjmlltqlqzzqgqcggdmdzznnnnsjjvbjjwbwhbhfhvvtmmsfmmcgmcmwcwhwnhhpccmbmdbmbgbjbggqqccfllfqqmqwwzbblffthhdnncqnccqppldlpldpllzmmsqqdffnggqlqtllwlglnlnhlhflfssvzzrllbtbnbgnnfvfllwslszswsnnpwwppvspsmmnfnpffrmrhmmctttrjrbjrjpjtpjpssdwdtwtmmtgtsgttlwttfrfvvpjpcjccmtthhldhllzslshhnrnvvfddnllltclcrrhnnjwwwpfpddmtmsmfflslrlmlmwmllgfgmfgmmjttpcpspslsjspsqstqsqqpsprphrrpqqfzqqwcwcddsjjpvvfnfvnnnrncnwcwczzcwzwnwmwffbdfbdfdjjhrhvhhvwvsvhshnhwwzlwlnnphhtjjmljjqzjjsjgsjshhwjjmttvgvsgstggrcrmmrqrhrqrzrmzmggqvqtqgtqqqqltqqwggmmzggjccgmgwgqqmnqnrnprptrrvfrvffnmnfmmnnnwzzldlvlgvlvqqpnphpgglhlshlhzzpcptpssblqvdbpbbcrngctqgptccwpdcpbcjwdmcrzmhwffgzqmmqwpqvplwzmjlzmvmzmbtqjnhzrpppnpntvmjbzmvhjvbgflmmjnwssvqvbnbddfcwqdtvpvddctmpptcjmvwszhbsttcbjlfjvwlljhlqlvvsnzphdjhfswltdhzprltzcszrgcmnmfznmbccstjvjngwpbsfqssfwvpdhhmlmzttzlszsgpvvbcfvzrlsttlqpnqhwtbqfjnbztnwfnhlhfltgdtsrrwrfhlssvsgzpffnnrhgcvclqnjgfhhzswllvcjffpngcmtjphwnbdfrrgjfrfqbnvbwgccsjvvmjgcvqvtggnvgvgnnchbblqnvvdgjtvdmfrzvhvhzcbqzdslphjjqtcwjqptstvvpqgdbgbcmmchjpvjhvbwtlmlnqpldfcbmwvrmpqcsfdhmmwnbvmpglcfbnsgjmljcwpzpwffcqfrbdrztzhqzhzpcrjfdmrctttdrzlmzcqwjftngwjmgqscftnpbjwqrcvqwbwbdhbhvrdcvgrvctjgwjtmdgzwgvdbmsrjpsbhwcqlqzjnzmgpctlwqhfnbmgsprjcqtfjjvzljqpfqgnvrgnjjlmpqgnzpmpsvzjmtvnfgslldjtjdwlzrvqrbvcpspzpcdnpdjmhcdhsbmthmgjqchqwwsnfjnwgpctlwcdpqpmzqcrptscngqnmhzwjdcqwvdmlzntsfbstbtmmnlsspjbjjdspnslgcnlbfnbhjlzjhrrmdbbwtswqpbpwtzhcnldbsfrvndzvcgzjprcrclhfwbvzgthcglfzqrshgtvbflvnznhmlzdtfnrsltnnppqgrtndbsfqmftdnzmqfwdpcrmssldmrrnzchnqpflgbqzqjjrzlfnptqdwzdhmctfbztmfcmbqcwjmgnwgqzqjctphrrthgvpvppztvpzgzhdszfhlzlcnwmfrlsnvftfrlfvbnlwzctphhpfvszntqcvnfmvmwwhsjlnpfhcpjvrncgmsbprwwllvnsbjfhtbtmcvvpzcvqrrqdvgzvllvcvnvvbftngqcqcvvbsqfshmnhwptcsbsnjzltqzmflftrhblqszrzsbfcpgzncvwhlqlcbmgjdpfcmlgdfphsfcgqccthmlzjbdwpsbddwwrtwmsvqwbzwhzmghhrspvbptznqsqvhgnhlwqjnhgnzprrtjddwtqfsshjrvlglhdlstghftmllvzmmfglnscnrtgcwwwzjphzhvqlctdwjlqvbsvlgzrdpvjhhcthgjhlwsgfzlschhfprfcrzfrzmnlwvqsnqlllczwfhswchrlggqszwrvpldrffnzrffbhtfbslgcdrqpjcrbqsrgfrhttcptncfndcbsdbjsqjvgbmnmhlnbltdcgbmllpgjmgljvglrwmrvgthhhzrsmzvgwcfgvcsbzpjcqnhrzhznzjcjghhwqvllrmsvlpzlssrdsqwvzvqwsvfsjqvbgrfbmfzlchqsjgncbljtvzsfdnvmfzcbrlnnvvmjbmgjmqzjtdzpljdwqtvwsrlbslwfvlgbtnmlpcwmngncnmdhqctshmjmnhpqcqzhvlbvgptctrvggdgnpnrlnngrfhsqdfthvcnpwjfjnslcqlfrfvhnctmsqgnqmgpwtlzhtdqhqqrcllzjccnszsqvrzhcffvnfnstgdmljdrqrndljdnfbbjvmpqdnqhtdlnzcvnfjlvzmfzrndhtglvngmbrdbpbnhvfmrbcwqzttnjplgrhchjtfjwfbjfbmzlrnllhzccpfhfhnjpfvzlpbqnhwmpssvwtzhdbtnbtllhpfdcqjjnzgbdrfjjbcltnzdrmtmsmvpjtmdnqszgbqncsvhjbgwswhmghpvstrqbglgrtgbchttbznvvdhppzwnttpgcbdjdhlsqhhtlphjjrjncrmfdtjhdwmjgmpngnbptzwgwdztmhtpglnftwpnnmrmcwfhwnhlsbwsrjnlmdlmffbzsnhsvnbldwtrrhdhfsjdrsnzlgtfzcwwqrfhtrmjhmphqndwtbpczvmfgczmdlqjqdlwmvjjzwmqnpvwzmtjwtprlnbvjdhpjgndrwzcfthnwhnhqpwtcjlhrhdplzsncfmszmhjmgljhnlsrrfwplclcvjjqmtpnwbtsbwdnjdlqntvdnfgwbpwspssprbffjdlcvbwcqlttnwnhwdspfsjhppbhspnrvrsfmzvbwwtjfzmnzwgqddbmcjzzqhqlgrglsvgsjdwlnsbtmqgsnfwwqrjsbcgdlmbgqwvgpqllqwbcplfjrgnzsdtdtvqnrbcrqjhdtqqplvszvtlflgbpwnpzczbvhzfjrslcwcswsgfvvsswzzwhtfjfpsrvcfnrs")
}
