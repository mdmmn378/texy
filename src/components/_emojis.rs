fn get_emojis() -> Vec {
    let emojis = vec![
        "©️", "®️", " ‼️", "⁉️", "™️", " ℹ️", "↔️", " ↕️", "↖️", "↗️", "↘️", "↙️", "↩️", "↪️", "⌚️", "⌛️", "⌨️",
        "⏏️", " ⏩️", " ⏪️", " ⏫️", " ⏬️", " ⏭️", " ⏮️", " ⏯️", "⏰️", "⏱️", "⏲️", "⏳️", " ⏸️", " ⏹️", " ⏺️",
        "Ⓜ️", "▪️", "▫️", " ▶️", " ◀️", "◻️", "◼️", "◽️", "◾️", "☀️", "☁️", "☂️", "☃️", "☄️", "☎️", "☑️", "☔️",
        "☕️", "☘️", "☝️", "☠️", "☢️", "☣️", "☦️", "☪️", "☮️", "☯️", "☸️", "☹️", "☺️", "♀️", "♂️", "♈️", "♉️",
        "♊️", "♋️", "♌️", "♍️", "♎️", "♏️", "♐️", "♑️", "♒️", "♓️", "♟️", "♠️", "♣️", "♥️", "♦️", "♨️",
        "♻️", "♾️", "♿️", "⚒️", "⚓️", "⚔️", "⚕️", "⚖️", "⚗️", "⚙️", "⚛️", "⚜️", "⚠️", "⚡️", "⚧️", "⚪️", " ⚫️",
        "⚰️", "⚱️", "⚽️", "⚾️", "⛄️", "⛅️", "⛈️", "⛎️", "⛏️", "⛑️", "⛓️", "⛔️", "⛩️", "⛪️", "⛰️", "⛱️",
        "⛲️", "⛳️", "⛴️", "⛵️", "⛷️", "⛸️", "⛹️", "⛺️", "⛽️", "✂️", "✅️", "✈️", "✉️", "✊️", "✋️", "✌️",
        "✍️", "✏️", "✒️", "✔️", "✖️", "✝️", "✡️", "✨️", "✳️", "✴️", "❄️", "❇️", "❌️", "❎️", "❓️", "❔️", "❕️",
        "❗️", "❣️", "❤️", "➕️", "➖️", "➗️", "➡️", "➰️", "➿️", "⤴️", "⤵️", "⬅️", "⬆️", " ⬇️", "⬛️", "⬜️",
        "⭐️", "⭕️", "〰️", "〽️", "㊗️", "㊙️", "🀄", "🃏", "🅰️", "🅱️", "🅾️", "🅿️", "🆎", "🆑", "🆒", "🆓",
        "🆔", "🆕", "🆖", "🆗", "🆘", "🆙", "🆚", "🈁", "🈂️", "🈚", "🈯", "🈲", "🈳", "🈴", "🈵",
        "🈶", "🈷️", "🈸", "🈹", "🈺", "🉐", "🉑", "🌀", "🌁", "🌂", "🌃", "🌄", "🌅", "🌆", "🌇",
        "🌈", "🌉", "🌊", "🌋", "🌌", "🌍", "🌎", "🌏", "🌐", "🌑", "🌒", "🌓", "🌔", "🌕", "🌖",
        "🌗", "🌘", "🌙", "🌚", "🌛", "🌜", "🌝", "🌞", "🌟", "🌠", "🌡️", "🌤️", "🌥️", "🌦️", "🌧️", "🌨️",
        "🌩️", "🌪️", "🌫️", "🌬️", "🌭", "🌮", "🌯", "🌰", "🌱", "🌲", "🌳", "🌴", "🌵", "🌶️", "🌷", "🌸",
        "🌹", "🌺", "🌻", "🌼", "🌽", "🌾", "🌿", "🍀", "🍁", "🍂", "🍃", "🍄", "🍅", "🍆", "🍇",
        "🍈", "🍉", "🍊", "🍋", "🍌", "🍍", "🍎", "🍏", "🍐", "🍑", "🍒", "🍓", "🍔", "🍕", "🍖",
        "🍗", "🍘", "🍙", "🍚", "🍛", "🍜", "🍝", "🍞", "🍟", "🍠", "🍡", "🍢", "🍣", "🍤", "🍥",
        "🍦", "🍧", "🍨", "🍩", "🍪", "🍫", "🍬", "🍭", "🍮", "🍯", "🍰", "🍱", "🍲", "🍳", "🍴",
        "🍵", "🍶", "🍷", "🍸", "🍹", "🍺", "🍻", "🍼", "🍽️", "🍾", "🍿", "🎀", "🎁", "🎂", "🎃",
        "🎄", "🎅", "🎆", "🎇", "🎈", "🎉", "🎊", "🎋", "🎌", "🎍", "🎎", "🎏", "🎐", "🎑", "🎒",
        "🎓", "🎖️", "🎗️", "🎙️", "🎚️", "🎛️", "🎞️", "🎟️", "🎠", "🎡", "🎢", "🎣", "🎤", "🎥", "🎦", "🎧",
        "🎨", "🎩", "🎪", "🎫", "🎬", "🎭", "🎮", "🎯", "🎰", "🎱", "🎲", "🎳", "🎴", "🎵", "🎶",
        "🎷", "🎸", "🎹", "🎺", "🎻", "🎼", "🎽", "🎾", "🎿", "🏀", "🏁", "🏂", "🏃", "🏄", "🏅",
        "🏆", "🏇", "🏈", "🏉", "🏊", "🏋️", "🏌️", "🏍️", "🏎️", "🏏", "🏐", "🏑", "🏒", "🏓", "🏔️", "🏕️",
        "🏖️", "🏗️", "🏘️", "🏙️", "🏚️", "🏛️", "🏜️", "🏝️", "🏞️", "🏟️", "🏠", "🏡", "🏢", "🏣", "🏤", "🏥", "🏦",
        "🏧", "🏨", "🏩", "🏪", "🏫", "🏬", "🏭", "🏮", "🏯", "🏰", "🏳️", "🏴", "🏵️", "🏷️", "🏸",
        "🏹", "🏺", "🏻", "🏼", "🏽", "🏾", "🏿", "🐀", "🐁", "🐂", "🐃", "🐄", "🐅", "🐆", "🐇",
        "🐈", "🐉", "🐊", "🐋", "🐌", "🐍", "🐎", "🐏", "🐐", "🐑", "🐒", "🐓", "🐔", "🐕", "🐖",
        "🐗", "🐘", "🐙", "🐚", "🐛", "🐜", "🐝", "🐞", "🐟", "🐠", "🐡", "🐢", "🐣", "🐤", "🐥",
        "🐦", "🐧", "🐨", "🐩", "🐪", "🐫", "🐬", "🐭", "🐮", "🐯", "🐰", "🐱", "🐲", "🐳", "🐴",
        "🐵", "🐶", "🐷", "🐸", "🐹", "🐺", "🐻", "🐼", "🐽", "🐾", "🐿️", "👀", "👁️", "👂", "👃",
        "👄", "👅", "👆", "👇", "👈", "👉", "👊", "👋", "👌", "👍", "👎", "👏", "👐", "👑", "👒",
        "👓", "👔", "👕", "👖", "👗", "👘", "👙", "👚", "👛", "👜", "👝", "👞", "👟", "👠", "👡",
        "👢", "👣", "👤", "👥", "👦", "👧", "👨", "👩", "👪", "👫", "👬", "👭", "👮", "👯", "👰",
        "👱", "👲", "👳", "👴", "👵", "👶", "👷", "👸", "👹", "👺", "👻", "👼", "👽", "👾", "👿",
        "💀", "💁", "💂", "💃", "💄", "💅", "💆", "💇", "💈", "💉", "💊", "💋", "💌", "💍", "💎",
        "💏", "💐", "💑", "💒", "💓", "💔", "💕", "💖", "💗", "💘", "💙", "💚", "💛", "💜", "💝",
        "💞", "💟", "💠", "💡", "💢", "💣", "💤", "💥", "💦", "💧", "💨", "💩", "💪", "💫", "💬",
        "💭", "💮", "💯", "💰", "💱", "💲", "💳", "💴", "💵", "💶", "💷", "💸", "💹", "💺", "💻",
        "💼", "💽", "💾", "💿", "📀", "📁", "📂", "📃", "📄", "📅", "📆", "📇", "📈", "📉", "📊",
        "📋", "📌", "📍", "📎", "📏", "📐", "📑", "📒", "📓", "📔", "📕", "📖", "📗", "📘", "📙",
        "📚", "📛", "📜", "📝", "📞", "📟", "📠", "📡", "📢", "📣", "📤", "📥", "📦", "📧", "📨",
        "📩", "📪", "📫", "📬", "📭", "📮", "📯", "📰", "📱", "📲", "📳", "📴", "📵", "📶", "📷",
        "📸", "📹", "📺", "📻", "📼", "📽️", "📿", "🔀", "🔁", "🔂", "🔃", "🔄", "🔅", "🔆", "🔇",
        "🔈", "🔉", "🔊", "🔋", "🔌", "🔍", "🔎", "🔏", "🔐", "🔑", "🔒", "🔓", " 🔔", "🔕", "🔖",
        "🔗", "🔘", "🔙", "🔚", "🔛", "🔜", "🔝", "🔞", "🔟", "🔠", "🔡", "🔢", "🔣", "🔤", "🔥",
        "🔦", "🔧", "🔨", "🔩", "🔪", "🔫", "🔬", "🔭", "🔮", "🔯", "🔰", "🔱", "🔲", "🔳", "🔴",
        "🔵", "🔶", "🔷", "🔸", "🔹", "🔺", "🔻", "🔼", "🔽", "🕉️", "🕊️", "🕋", "🕌", "🕍", "🕎",
        "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛", "🕜", "🕝", "🕞",
        "🕟", "🕠", "🕡", "🕢", "🕣", "🕤", "🕥", "🕦", "🕧", "🕯️", "🕰️", "🕳️", "🕴️", "🕵️", "🕶️", "🕷️",
        "🕸️", "🕹️", "🕺", "🖇️", "🖊️", "🖋️", "🖌️", "🖍️", "🖐️", "🖕", "🖖", "🖤", "🖥️", "🖨️", "🖱️", "🖲️", "🖼️",
        "🗂️", "🗃️", "🗄️", "🗑️", "🗒️", "🗓️", "🗜️", "🗝️", "🗞️", "🗡️", "🗣️", "🗨️", "🗯️", "🗳️", "🗺️", "🗻", "🗼",
        "🗽", "🗾", "🗿", "😀", "😁", "😂", "😃", "😄", "😅", "😆", "😇", "😈", "😉", "😊", "😋",
        "😌", "😍", "😎", "😏", "😐", "😑", "😒", "😓", "😔", "😕", "😖", "😗", "😘", "😙", "😚",
        "😛", "😜", "😝", "😞", "😟", "😠", "😡", "😢", "😣", "😤", "😥", "😦", "😧", "😨", "😩",
        "😪", "😫", "😬", "😭", "😮", "😯", "😰", "😱", "😲", "😳", "😴", "😵", "😶", "😷", "😸",
        "😹", "😺", "😻", "😼", "😽", "😾", "😿", "🙀", "🙁", "🙂", "🙃", "🙄", "🙅", "🙆", "🙇",
        "🙈", "🙉", "🙊", "🙋", "🙌", "🙍", "🙎", "🙏", "🚀", "🚁", "🚂", "🚃", "🚄", "🚅", "🚆",
        "🚇", "🚈", "🚉", "🚊", "🚋", "🚌", "🚍", "🚎", "🚏", "🚐", "🚑", "🚒", "🚓", "🚔", "🚕",
        "🚖", "🚗", "🚘", "🚙", "🚚", "🚛", "🚜", "🚝", "🚞", "🚟", "🚠", "🚡", "🚢", "🚣", "🚤",
        "🚥", "🚦", "🚧", "🚨", "🚩", "🚪", "🚫", "🚬", "🚭", "🚮", "🚯", "🚰", "🚱", "🚲", "🚳",
        "🚴", "🚵", "🚶", "🚷", "🚸", "🚹", "🚺", "🚻", "🚼", "🚽", "🚾", "🚿", "🛀", "🛁", "🛂",
        "🛃", "🛄", "🛅", "🛋️", "🛌", "🛍️", "🛎️", "🛏️", "🛐", "🛑", "🛒", "🛕", "🛖", "🛗", "🛜", "🛝",
        "🛞", "🛟", "🛠️", "🛡️", "🛢️", "🛣️", "🛤️", "🛥️", "🛩️", "🛫", "🛬", "🛰️", "🛳️", "🛴", "🛵", "🛶", "🛷",
        "🛸", "🛹", "🛺", "🛻", "🛼", "🟠", "🟡", "🟢", "🟣", "🟤", "🟥", "🟦", "🟧", "🟨", "🟩",
        "🟪", "🟫", "🟰", "🤌", "🤍", "🤎", "🤏", "🤐", "🤑", "🤒", "🤓", "🤔", "🤕", "🤖", "🤗",
        "🤘", "🤙", "🤚", "🤛", "🤜", "🤝", "🤞", "🤟", "🤠", "🤡", "🤢", "🤣", "🤤", "🤥", "🤦",
        "🤧", "🤨", "🤩", "🤪", "🤫", "🤬", "🤭", "🤮", "🤯", "🤰", "🤱", "🤲", "🤳", "🤴", "🤵",
        "🤶", "🤷", "🤸", "🤹", "🤺", "🤼", "🤽", "🤾", "🤿", "🥀", "🥁", "🥂", "🥃", "🥄", "🥅",
        "🥇", "🥈", "🥉", "🥊", "🥋", "🥌", "🥍", "🥎", "🥏", "🥐", "🥑", "🥒", "🥓", "🥔", "🥕",
        "🥖", "🥗", "🥘", "🥙", "🥚", "🥛", "🥜", "🥝", "🥞", "🥟", "🥠", "🥡", "🥢", "🥣", "🥤",
        "🥥", "🥦", "🥧", "🥨", "🥩", "🥪", "🥫", "🥬", "🥭", "🥮", "🥯", "🥰", "🥱", "🥲", "🥳",
        "🥴", "🥵", "🥶", "🥷", "🥸", "🥹", "🥺", "🥻", "🥼", "🥽", "🥾", "🥿", "🦀", "🦁", "🦂",
        "🦃", "🦄", "🦅", "🦆", "🦇", "🦈", "🦉", "🦊", "🦋", "🦌", "🦍", "🦎", "🦏", "🦐", "🦑",
        "🦒", "🦓", "🦔", "🦕", "🦖", "🦗", "🦘", "🦙", "🦚", "🦛", "🦜", "🦝", "🦞", "🦟", "🦠",
        "🦡", "🦢", "🦣", "🦤", "🦥", "🦦", "🦧", "🦨", "🦩", "🦪", "🦫", "🦬", "🦭", "🦮", "🦯",
        "🦰", "🦱", "🦲", "🦳", "🦴", "🦵", "🦶", "🦷", "🦸", "🦹", "🦺", "🦻", "🦼", "🦽", "🦾",
        "🦿", "🧀", "🧁", "🧂", "🧃", "🧄", "🧅", "🧆", "🧇", "🧈", "🧉", "🧊", "🧋", "🧌", "🧍",
        "🧎", "🧏", "🧐", "🧑", "🧒", "🧓", "🧔", "🧕", "🧖", "🧗", "🧘", "🧙", "🧚", "🧛", "🧜",
        "🧝", "🧞", "🧟", "🧠", "🧡", "🧢", "🧣", "🧤", "🧥", "🧦", "🧧", "🧨", "🧩", "🧪", "🧫",
        "🧬", "🧭", "🧮", "🧯", "🧰", "🧱", "🧲", "🧳", "🧴", "🧵", "🧶", "🧷", "🧸", "🧹", "🧺",
        "🧻", "🧼", "🧽", "🧾", "🧿", "🩰", "🩱", "🩲", "🩳", "🩴", "🩵", "🩶", "🩷", "🩸", "🩹",
        "🩺", "🩻", "🩼", "🪀", "🪁", "🪂", "🪃", "🪄", "🪅", "🪆", "🪐", "🪑", "🪒", "🪓", "🪔",
        "🪕", "🪖", "🪗", "🪘", "🪙", "🪚", "🪛", "🪜", "🪝", "🪞", "🪟", "🪠", "🪡", "🪢", "🪣",
        "🪤", "🪥", "🪦", "🪧", "🪨", "🪩", "🪪", "🪫", "🪬", "🪰", "🪱", "🪲", "🪳", "🪴", "🪵", "🪶",
        "🪷", "🪸", "🪹", "🪺", "🫀", "🫁", "🫂", "🫃", "🫄", "🫅", "🫎", "🫏", "🫐", "🫑", "🫒", "🫓",
        "🫔", "🫕", "🫖", "🫗", "🫘", "🫙", "🫠", "🫡", "🫢", "🫣", "🫤", "🫥", "🫦", "🫧", "🫰", "🫱", "🫲",
        "🫳", "🫴", "🫵", "🫶",
    ];
}