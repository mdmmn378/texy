// Tests

mod tests {
    use texy::components::actions::*;
    use texy::pipelines::blocks::*;
    #[test]
    fn test_remove_newlines() {
        let test_input = String::from("hello\nmello");
        let expected_output = String::from("hello mello");
        assert_eq!(remove_newlines(test_input), expected_output);
    }

    #[test]
    fn test_remove_infrequent_punctuations() {
        let test_input = String::from("hello %^&mello");
        let expected_output = String::from("hello mello");
        assert_eq!(remove_infrequent_punctuations(test_input), expected_output);
    }

    #[test]
    fn test_merge_spaces() {
        let test_input = String::from("hello   \t \nmello");
        let expected_output = String::from("hello mello");
        assert_eq!(merge_spaces(test_input), expected_output);
    }

    #[test]
    fn test_remove_emojis() {
        let mut test_input = String::from("This 🐕 dog 😂");
        let mut expected_output = String::from("This  dog ");
        assert_eq!(remove_emojis(test_input), expected_output);
        test_input = String::from("কুত্তার বাচ্চা 😂");
        expected_output = String::from("কুত্তার বাচ্চা ");
        assert_eq!(remove_emojis(test_input), expected_output);
    }

    #[test]
    fn test_remove_all_punctuations() {
        let test_input = String::from("hello!,. mello?");
        let expected_output = String::from("hello   mello");
        assert_eq!(remove_all_punctuations(test_input), expected_output);
    }

    #[test]
    fn test_relaxed() {
        let test_input = vec![String::from("hello\t\n")];
        let expected_output = vec![String::from("hello")];
        assert_eq!(relaxed(test_input), expected_output);
    }

    #[test]
    fn test_strict() {
        let test_input = vec![String::from("hello\t\n")];
        let expected_output = vec![String::from("hello")];
        assert_eq!(strict(test_input), expected_output);
    }

    #[test]
    fn test_extreme() {
        let test_input = vec![String::from("hello\t\n")];
        let expected_output = vec![String::from("hello")];
        assert_eq!(extreme(test_input), expected_output);
    }
}
