#!/usr/bin/env node
/*
 * Generator for content/plans/watchman-90.json
 * ----------------------------------------------
 * The full 90-day curriculum is large and repetitive to hand-edit, so it is
 * generated from curated arrays here and the output is committed. Re-run with:
 *
 *     node scripts/build-watchman-90.js
 *
 * Design:
 *  - Preserves the plan metadata, readings/disciplines definitions, the weekly
 *    LBCF 1689 confession_anchors, and the graduation block from the existing
 *    file (read at build time, never re-typed).
 *  - Each of the five reading tracks is a curated arc. Days 1-7 reproduce the
 *    original hand-authored sample week exactly (the arcs are seeded with those
 *    seven entries), then continue. Tracks shorter than 90 entries cycle, which
 *    is deliberate: cornerstone passages are worth re-reading across 90 days
 *    (the same design the Proverbs/Morning Wisdom track already used).
 *  - Reflection prompts are authored in 13 weekly blocks themed to that week's
 *    confession anchor, so the nightly examination echoes the doctrine of the
 *    week. 90 distinct prompts, none blank.
 */

const fs = require('fs');
const path = require('path');

const PLAN_PATH = path.join(__dirname, '..', 'content/plans/watchman-90.json');
const existing = JSON.parse(fs.readFileSync(PLAN_PATH, 'utf8'));

// ── Morning Wisdom: Proverbs 1-31, cycled, with a short note per chapter ──
const proverbsNotes = {
  1:  'The fear of the LORD is the beginning of knowledge.',
  2:  'Seek her as silver, search for her as hidden treasure.',
  3:  'Trust in the LORD with all your heart.',
  4:  'Keep your heart with all vigilance.',
  5:  'Rejoice in the wife of your youth.',
  6:  'Go to the ant, O sluggard; consider her ways.',
  7:  'Keep my commandments and live.',
  8:  'Wisdom calls aloud in the street.',
  9:  'The fear of the LORD is the beginning of wisdom.',
  10: 'The mouth of the righteous is a fountain of life.',
  11: 'When pride comes, then comes disgrace.',
  12: 'Whoever loves discipline loves knowledge.',
  13: 'Whoever walks with the wise becomes wise.',
  14: 'The wise woman builds her house.',
  15: 'A soft answer turns away wrath.',
  16: 'Commit your work to the LORD, and your plans will be established.',
  17: 'A friend loves at all times.',
  18: 'The name of the LORD is a strong tower.',
  19: 'Better a poor man who walks in integrity.',
  20: 'A righteous man walks in his integrity; blessed are his children after him.',
  21: 'The king\'s heart is a stream of water in the hand of the LORD.',
  22: 'A good name is to be chosen rather than great riches.',
  23: 'Do not toil to acquire wealth; be discerning enough to desist.',
  24: 'By wisdom a house is built, and by understanding it is established.',
  25: 'Whoever has no rule over his own spirit is like a city broken into.',
  26: 'Like a dog that returns to his vomit is a fool who repeats his folly.',
  27: 'Iron sharpens iron, and one man sharpens another.',
  28: 'The righteous are bold as a lion.',
  29: 'The fear of man lays a snare, but whoever trusts in the LORD is safe.',
  30: 'Every word of God proves true; He is a shield to those who take refuge in Him.',
  31: 'An excellent wife who can find? She is far more precious than jewels.',
};
function morningWisdom(day) {
  const chap = ((day - 1) % 31) + 1;
  return { ref: 'Proverbs ' + chap, note: proverbsNotes[chap] };
}
// Day 90 keeps its bespoke closing note.
const morningWisdomOverrides = {
  90: { ref: 'Proverbs 28', note: 'Day 90. The righteous are bold as a lion. Stand your post. Hold the line.' },
};

// ── Husband's Post — a marriage arc. Index 0-6 == original days 1-7. ──
const husbandsPost = [
  { ref: 'Ephesians 5:22-33', note: 'Love her as Christ loved the church.' },
  { ref: '1 Peter 3:7', note: 'Live with your wife in an understanding way.' },
  { ref: 'Colossians 3:18-19', note: 'Husbands, love your wives and do not be harsh with them.' },
  { ref: 'Proverbs 5:15-20', note: 'Drink water from your own cistern.' },
  { ref: 'Song of Solomon 2', note: 'My beloved is mine and I am his.' },
  { ref: '1 Corinthians 13', note: 'Love is patient, love is kind.' },
  { ref: 'Genesis 2:18-25', note: 'It is not good that the man should be alone.' },
  // continue the arc
  { ref: 'Ephesians 5:25-27', note: 'Christ gave Himself up to sanctify her.' },
  { ref: 'Genesis 24:62-67', note: 'Isaac loved Rebekah, and was comforted.' },
  { ref: 'Proverbs 18:22', note: 'He who finds a wife finds a good thing.' },
  { ref: 'Malachi 2:13-16', note: 'Guard yourselves; let none be faithless to the wife of his youth.' },
  { ref: 'Hebrews 13:4', note: 'Let marriage be held in honor among all.' },
  { ref: '1 Thessalonians 4:3-8', note: 'This is the will of God, your sanctification.' },
  { ref: 'Proverbs 31:10-12', note: 'The heart of her husband trusts in her.' },
  { ref: 'Song of Solomon 4:9-12', note: 'You have captivated my heart, my bride.' },
  { ref: '1 Corinthians 7:1-5', note: 'Do not deprive one another.' },
  { ref: 'Ephesians 5:28-30', note: 'He who loves his wife loves himself.' },
  { ref: 'Proverbs 19:14', note: 'A prudent wife is from the LORD.' },
  { ref: 'Ruth 1:16-17', note: 'Where you go I will go.' },
  { ref: '1 Peter 3:1-6', note: 'The imperishable beauty of a gentle and quiet spirit.' },
  { ref: 'Titus 2:6-8', note: 'Show yourself a model of good works.' },
  { ref: 'Song of Solomon 8:6-7', note: 'Love is strong as death; many waters cannot quench it.' },
  { ref: '1 Corinthians 6:18-20', note: 'Flee from sexual immorality. You were bought with a price.' },
  { ref: 'Proverbs 12:4', note: 'An excellent wife is the crown of her husband.' },
  { ref: 'Ephesians 4:31-32', note: 'Be kind to one another, tenderhearted, forgiving.' },
  { ref: 'Colossians 3:12-14', note: 'Above all put on love, which binds everything together.' },
  { ref: 'Matthew 19:4-6', note: 'What God has joined together, let not man separate.' },
  { ref: 'Philippians 2:3-4', note: 'Count others more significant than yourselves.' },
  { ref: '1 John 4:7-12', note: 'If God so loved us, we also ought to love one another.' },
  { ref: 'Psalm 128', note: 'Your wife will be like a fruitful vine within your house.' },
  { ref: 'Proverbs 21:9', note: 'Better to live on a corner of the housetop than in a house shared with a quarrelsome wife — guard the peace.' },
  { ref: 'Song of Solomon 1:2-4', note: 'Draw me after you; let us run.' },
  { ref: 'Genesis 29:18-20', note: 'They seemed but a few days because of the love he had for her.' },
  { ref: 'Hosea 3:1', note: 'Love a woman as the LORD loves the children of Israel.' },
  { ref: 'Ecclesiastes 9:9', note: 'Enjoy life with the wife whom you love.' },
  { ref: '1 Corinthians 16:14', note: 'Let all that you do be done in love.' },
  { ref: 'Romans 12:9-10', note: 'Let love be genuine; outdo one another in showing honor.' },
  { ref: 'Proverbs 14:1', note: 'The wisest of women builds her house — build alongside her.' },
  { ref: 'Ephesians 5:1-2', note: 'Walk in love, as Christ loved us and gave Himself up.' },
  { ref: 'Isaiah 54:5', note: 'Your Maker is your husband — love as you have been loved.' },
  { ref: '1 Peter 4:8', note: 'Above all, keep loving one another earnestly.' },
  { ref: 'Proverbs 27:15-16', note: 'Restrain contention before it begins.' },
  { ref: '2 Corinthians 11:2', note: 'Betrothed to one husband, to present you as a pure bride to Christ.' },
  { ref: 'John 2:1-11', note: 'Christ blessed a wedding with His first sign.' },
  { ref: 'Revelation 19:6-9', note: 'Blessed are those invited to the marriage supper of the Lamb.' },
];

// ── Father's Charge — a fatherhood/legacy arc. Index 0-6 == days 1-7. ──
const fathersCharge = [
  { ref: 'Deuteronomy 6:1-9', note: 'Teach them diligently to your children.' },
  { ref: 'Deuteronomy 4:9', note: 'Keep your soul diligently; make them known to your children.' },
  { ref: 'Psalm 78:1-8', note: 'Tell the next generation the glorious deeds of the LORD.' },
  { ref: 'Proverbs 22:6', note: 'Train up a child in the way he should go.' },
  { ref: 'Ephesians 6:4', note: 'Fathers, do not provoke your children to anger.' },
  { ref: '1 Timothy 3:4-5', note: 'He must manage his own household well.' },
  { ref: 'Joshua 24:15', note: 'As for me and my house, we will serve the LORD.' },
  // continue the arc
  { ref: 'Psalm 127:3-5', note: 'Children are a heritage from the LORD.' },
  { ref: 'Proverbs 13:24', note: 'Whoever loves his son is diligent to discipline him.' },
  { ref: 'Hebrews 12:7-11', note: 'The Lord disciplines the one He loves.' },
  { ref: 'Genesis 18:19', note: 'Abraham will command his children to keep the way of the LORD.' },
  { ref: '2 Timothy 1:5', note: 'The sincere faith that dwelt first in your grandmother and mother.' },
  { ref: 'Proverbs 3:11-12', note: 'Do not despise the LORD\'s discipline.' },
  { ref: '1 Chronicles 28:9', note: 'Know the God of your father and serve Him.' },
  { ref: 'Exodus 12:26-27', note: 'When your children ask, you shall tell them.' },
  { ref: 'Proverbs 23:13-14', note: 'Do not withhold discipline from a child.' },
  { ref: 'Psalm 103:13', note: 'As a father shows compassion to his children.' },
  { ref: 'Deuteronomy 11:18-21', note: 'Teach them to your children, talking of them.' },
  { ref: 'Proverbs 20:7', note: 'The righteous who walks in his integrity — blessed are his children.' },
  { ref: 'Luke 15:20-24', note: 'While he was still far off, his father saw him and ran.' },
  { ref: '2 Timothy 3:14-15', note: 'From childhood you have been acquainted with the sacred writings.' },
  { ref: 'Proverbs 17:6', note: 'Grandchildren are the crown of the aged.' },
  { ref: 'Malachi 4:6', note: 'He will turn the hearts of fathers to their children.' },
  { ref: 'Proverbs 4:1-9', note: 'Hear, O sons, a father\'s instruction.' },
  { ref: '1 Kings 2:1-4', note: 'Be strong, and show yourself a man.' },
  { ref: 'Job 1:5', note: 'Job would rise early to intercede for his children.' },
  { ref: 'Genesis 48:15-16', note: 'The God who has been my shepherd, bless the boys.' },
  { ref: 'Psalm 145:4', note: 'One generation shall commend Your works to another.' },
  { ref: 'Proverbs 29:17', note: 'Discipline your son, and he will give you rest.' },
  { ref: 'Colossians 3:21', note: 'Do not provoke your children, lest they become discouraged.' },
  { ref: '1 Thessalonians 2:11-12', note: 'Like a father with his children, we exhorted you.' },
  { ref: 'Luke 2:41-52', note: 'He went down with them and was submissive.' },
  { ref: 'Deuteronomy 32:46-47', note: 'Command your children to be careful to do all this word.' },
  { ref: 'Proverbs 19:18', note: 'Discipline your son, for there is hope.' },
  { ref: '3 John 1:4', note: 'No greater joy than to hear my children walk in the truth.' },
  { ref: 'Psalm 34:11', note: 'Come, O children, listen to me; I will teach you the fear of the LORD.' },
  { ref: 'Proverbs 14:26', note: 'His children will have a refuge.' },
  { ref: '2 Timothy 2:1-2', note: 'Entrust to faithful men who will teach others also.' },
  { ref: 'Acts 2:39', note: 'The promise is for you and for your children.' },
  { ref: 'Genesis 17:7', note: 'An everlasting covenant, to be God to you and your offspring.' },
  { ref: 'Ephesians 6:1-3', note: 'Honor your father and mother — the first commandment with a promise.' },
  { ref: 'Proverbs 31:1-9', note: 'The words of King Lemuel, which his mother taught him.' },
  { ref: 'Psalm 128:1-4', note: 'Blessed is everyone who fears the LORD.' },
  { ref: 'Isaiah 38:19', note: 'The father makes known to the children Your faithfulness.' },
  { ref: 'Joel 1:3', note: 'Tell your children of it, and let your children tell their children.' },
];

// ── Citizen's Stand — courage, civic righteousness, soldiering. Index 0-6 == days 1-7. ──
const citizensStand = [
  { ref: "Ezekiel 33:1-9", note: "Set as a watchman: sound the trumpet, or their blood is on your hands." },
  { ref: "Ezekiel 3:16-21", note: "I have made you a watchman for the house of Israel." },
  { ref: "Ezekiel 2:1-7", note: "Son of man, stand on your feet; speak whether they hear or refuse." },
  { ref: "Ezekiel 22:30", note: "I sought a man to stand in the gap before Me, but found none." },
  { ref: "Daniel 1:8-21", note: "Daniel resolved that he would not defile himself." },
  { ref: "Jeremiah 1:4-10", note: "Before I formed you in the womb I knew you; I appoint you over nations." },
  { ref: "Ezekiel 1:1-3,26-28", note: "The likeness of the glory of the LORD by the river Chebar." },
  { ref: "Ezekiel 34:1-10", note: "Woe to the shepherds who feed themselves and not the flock." },
  { ref: "Ezekiel 34:11-16", note: "I Myself will search for My sheep and seek them out." },
  { ref: "Ezekiel 36:24-28", note: "A new heart I will give you, and a new spirit I will put within you." },
  { ref: "Ezekiel 37:1-14", note: "Son of man, can these dry bones live? Prophesy to the breath." },
  { ref: "Ezekiel 18:30-32", note: "Repent and turn; why will you die, O house of Israel?" },
  { ref: "Ezekiel 33:10-20", note: "I have no pleasure in the death of the wicked, but that he turn and live." },
  { ref: "Ezekiel 13:1-9", note: "Woe to the prophets who have not gone up into the breaches." },
  { ref: "Ezekiel 11:16-20", note: "I will give them one heart and put a new spirit within them." },
  { ref: "Ezekiel 14:12-20", note: "Though Noah, Daniel, and Job were in it, they would deliver but themselves." },
  { ref: "Ezekiel 16:60-63", note: "I will remember My covenant and establish an everlasting covenant." },
  { ref: "Ezekiel 20:40-44", note: "You shall know that I am the LORD, when I deal with you for My name's sake." },
  { ref: "Ezekiel 43:1-7", note: "The glory of the LORD filled the temple." },
  { ref: "Ezekiel 47:1-12", note: "The river from the temple: everything will live where it flows." },
  { ref: "Daniel 2:20-23", note: "He changes times and seasons; He removes kings and sets up kings." },
  { ref: "Daniel 3:16-18", note: "Our God is able to deliver us; but if not, we will not serve your gods." },
  { ref: "Daniel 4:34-37", note: "Those who walk in pride He is able to humble." },
  { ref: "Daniel 6:10", note: "He got down on his knees three times a day, as he had done before." },
  { ref: "Daniel 7:13-14", note: "To the Son of Man was given dominion and a kingdom that shall not pass away." },
  { ref: "Daniel 9:3-19", note: "O Lord, hear; O Lord, forgive; for Your own sake, O my God." },
  { ref: "Daniel 12:1-3", note: "Those who are wise shall shine like the brightness of the sky." },
  { ref: "Jeremiah 6:16", note: "Stand by the roads; ask for the ancient paths, and walk in them." },
  { ref: "Jeremiah 7:1-7", note: "Amend your ways; do not trust in deceptive words." },
  { ref: "Jeremiah 17:5-8", note: "Blessed is the man who trusts in the LORD, like a tree planted by water." },
  { ref: "Jeremiah 18:1-6", note: "Like clay in the potter's hand, so are you in My hand." },
  { ref: "Jeremiah 20:9", note: "His word is in my heart like a burning fire shut up in my bones." },
  { ref: "Jeremiah 23:1-6", note: "Woe to the shepherds who scatter; I will raise up a righteous Branch." },
  { ref: "Jeremiah 29:4-7", note: "Seek the welfare of the city where I have sent you." },
  { ref: "Jeremiah 31:31-34", note: "A new covenant: I will write My law on their hearts." },
  { ref: "Lamentations 3:22-26", note: "His mercies are new every morning; great is Your faithfulness." },
  { ref: "1 Corinthians 16:13", note: "Be watchful, stand firm, act like men, be strong." },
  { ref: "Ephesians 6:10-18", note: "Put on the whole armor of God; stand against the schemes of the devil." },
  { ref: "Acts 5:29", note: "We must obey God rather than men." },
  { ref: "Matthew 5:13-16", note: "You are the salt of the earth and the light of the world." },
  { ref: "2 Timothy 4:1-5", note: "Preach the word; be ready in season and out of season." },
  { ref: "Hebrews 13:5-6", note: "The Lord is my helper; I will not fear what man can do to me." },
  { ref: "1 Peter 3:14-16", note: "Honor Christ as holy, always ready to give a defense for the hope in you." },
  { ref: "Revelation 2:10", note: "Be faithful unto death, and I will give you the crown of life." },
];

// ── Evening Peace — a psalm for the night. Index 0-6 == days 1-7. ──
const eveningPeace = [
  { ref: 'Psalm 1', note: 'Blessed is the man who walks not in the counsel of the wicked.' },
  { ref: 'Psalm 23', note: 'The LORD is my shepherd.' },
  { ref: 'Psalm 46', note: 'Be still and know that I am God.' },
  { ref: 'Psalm 91', note: 'He who dwells in the shelter of the Most High.' },
  { ref: 'Psalm 103', note: 'Bless the LORD, O my soul.' },
  { ref: 'Psalm 121', note: 'I lift up my eyes to the hills.' },
  { ref: 'Psalm 139', note: 'Search me, O God, and know my heart.' },
  // continue
  { ref: 'Psalm 4', note: 'In peace I will both lie down and sleep.' },
  { ref: 'Psalm 3', note: 'I lay down and slept; I woke again, for the LORD sustained me.' },
  { ref: 'Psalm 8', note: 'What is man that You are mindful of him?' },
  { ref: 'Psalm 16', note: 'You make known to me the path of life.' },
  { ref: 'Psalm 19', note: 'The heavens declare the glory of God.' },
  { ref: 'Psalm 27', note: 'The LORD is my light and my salvation; whom shall I fear?' },
  { ref: 'Psalm 30', note: 'Weeping may tarry for the night, but joy comes with the morning.' },
  { ref: 'Psalm 32', note: 'Blessed is the one whose transgression is forgiven.' },
  { ref: 'Psalm 34', note: 'I sought the LORD, and He answered me.' },
  { ref: 'Psalm 37', note: 'Commit your way to the LORD; trust in Him.' },
  { ref: 'Psalm 40', note: 'He drew me up from the pit and set my feet upon a rock.' },
  { ref: 'Psalm 42', note: 'As a deer pants for flowing streams.' },
  { ref: 'Psalm 51', note: 'Create in me a clean heart, O God.' },
  { ref: 'Psalm 62', note: 'For God alone my soul waits in silence.' },
  { ref: 'Psalm 63', note: 'My soul thirsts for You; my flesh faints for You.' },
  { ref: 'Psalm 84', note: 'A day in Your courts is better than a thousand elsewhere.' },
  { ref: 'Psalm 90', note: 'Teach us to number our days, that we may get a heart of wisdom.' },
  { ref: 'Psalm 95', note: 'Come, let us worship and bow down.' },
  { ref: 'Psalm 96', note: 'Sing to the LORD a new song.' },
  { ref: 'Psalm 100', note: 'Enter His gates with thanksgiving.' },
  { ref: 'Psalm 107', note: 'Give thanks to the LORD, for He is good.' },
  { ref: 'Psalm 116', note: 'I love the LORD, because He has heard my voice.' },
  { ref: 'Psalm 118', note: 'This is the day the LORD has made.' },
  { ref: 'Psalm 119:105-112', note: 'Your word is a lamp to my feet.' },
  { ref: 'Psalm 130', note: 'Out of the depths I cry to You, O LORD.' },
  { ref: 'Psalm 131', note: 'I have calmed and quieted my soul.' },
  { ref: 'Psalm 133', note: 'How good and pleasant when brothers dwell in unity.' },
  { ref: 'Psalm 136', note: 'His steadfast love endures forever.' },
  { ref: 'Psalm 138', note: 'I give You thanks, O LORD, with my whole heart.' },
  { ref: 'Psalm 143', note: 'In the morning let me hear of Your steadfast love.' },
  { ref: 'Psalm 145', note: 'Great is the LORD, and greatly to be praised.' },
  { ref: 'Psalm 146', note: 'Praise the LORD, O my soul.' },
  { ref: 'Psalm 147', note: 'He heals the brokenhearted and binds up their wounds.' },
  { ref: 'Psalm 148', note: 'Praise Him, sun and moon, all you shining stars.' },
  { ref: 'Psalm 150', note: 'Let everything that has breath praise the LORD.' },
  { ref: 'Psalm 73', note: 'Whom have I in heaven but You?' },
  { ref: 'Psalm 27:13-14', note: 'Wait for the LORD; be strong, let your heart take courage.' },
  { ref: 'Psalm 18:1-3', note: 'I love You, O LORD, my strength.' },
  // Gospels — the peace of Christ
  { ref: "Matthew 11:28-30", note: "Come to Me, all who labor; My yoke is easy and My burden is light." },
  { ref: "John 14:1-3", note: "Let not your hearts be troubled; I go to prepare a place for you." },
  { ref: "John 14:27", note: "Peace I leave with you; My peace I give to you." },
  { ref: "Matthew 6:25-34", note: "Do not be anxious; seek first the kingdom of God." },
  { ref: "Philippians 4:4-9", note: "The peace of God will guard your hearts and minds in Christ Jesus." },
  { ref: "Romans 8:31-39", note: "Nothing can separate us from the love of God in Christ Jesus." },
];

// Evening Peace finale — Revelation across the graduation week (days 85-90).
const eveningPeaceOverrides = {
  85: { ref: "Revelation 1:9-18", note: "Fear not, I am the first and the last, the living One." },
  86: { ref: "Revelation 5:9-14", note: "Worthy is the Lamb who was slain." },
  87: { ref: "Revelation 7:9-17", note: "He will wipe away every tear from their eyes." },
  88: { ref: "Revelation 19:6-9", note: "Blessed are those invited to the marriage supper of the Lamb." },
  89: { ref: "Revelation 21:1-7", note: "Behold, I am making all things new." },
  90: { ref: "Revelation 22:1-5,20", note: "No more night; they shall reign forever. Come, Lord Jesus." },
};

// ── Reflection prompts, 13 weekly blocks themed to the confession anchor. ──
// Weeks 1-12 have 7 prompts; week 13 has 6 (days 85-90).
const promptWeeks = [
  // Week 1 — Of the Holy Scriptures (original sample week, preserved)
  [
    'What post has God assigned you today? What does it mean to stand there?',
    'Where did you compromise today? Where did you hold the line?',
    'What did the fast show you that fullness was hiding?',
    'Who did you fail to love today as Christ loves the church?',
    'If your son were watching you this week, what would he learn about being a man?',
    'Where did you fear man more than God today?',
    'What has God done this week that you almost missed?',
  ],
  // Week 2 — Of God and the Holy Trinity
  [
    'Did you live today as though God were truly watching — Father, Son, and Spirit?',
    'Where did you treat God as small today? What does His infinitude correct in you?',
    'The Spirit indwells you. Where did you grieve Him today, and where did you yield?',
    'You serve a God of three Persons in perfect love. Did your home reflect that love or contradict it?',
    'What did you trust today more than the living God?',
    'Where did you speak to the Father as a son, and where did you forget you could?',
    'This Lord\'s Day, did you worship the God who is, or one you have shrunk to fit you?',
  ],
  // Week 3 — Of the Fall, of Sin
  [
    'Name the sin that surfaced today. Did you excuse it or kill it?',
    'Where did you feel the pull of the old man, dead in trespasses, still grasping?',
    'What did your fasting expose about your appetites today?',
    'Where did pride wear the mask of principle today?',
    'You are not as sick as sin would make you, nor as well as you pretend. Which lie tempted you more today?',
    'Where did you blame another for what was your own corruption?',
    'What sin do you most want hidden? Bring it into the light this Lord\'s Day.',
  ],
  // Week 4 — Of Christ the Mediator
  [
    'You have one Mediator. Where did you try to mediate for yourself today?',
    'Christ is your Prophet — did you listen to His word, or your own?',
    'Christ is your Priest — what did you carry today that He already bore?',
    'Christ is your King — where did you refuse His rule today?',
    'Where did you need an Advocate today, and did you remember you have one?',
    'What burden are you carrying that the Mediator has already settled?',
    'This Lord\'s Day, look away from yourself to Christ. What do you see?',
  ],
  // Week 5 — Of Justification
  [
    'Did you work today from acceptance, or for it?',
    'Your standing is not your streak. Where did you forget that today?',
    'Whose righteousness were you resting in when you lay down tonight?',
    'Where did failure today tempt you to doubt a verdict already rendered?',
    'You are counted righteous in Christ. Did that free you to confess, or did shame silence you?',
    'What did you do today to earn what was already given?',
    'This Lord\'s Day: rest. The work that justifies you is finished. Do you believe it?',
  ],
  // Week 6 — Of Sanctification
  [
    'These disciplines are means of grace, not means of merit. Did you treat them as the first or the second today?',
    'Where did the Spirit grow something in you this week that you did not manufacture?',
    'What dominion of sin is weaker now than on Day 1? What is not?',
    'Where did you cooperate with grace today, and where did you resist it?',
    'Holiness is not behavior alone. Where did your heart need changing, not just your hands?',
    'What ordinary means — Word, prayer, fellowship — did you neglect today?',
    'This Lord\'s Day, where do you see God conforming you to Christ, slowly?',
  ],
  // Week 7 — Of Saving Faith
  [
    'Where did you walk by sight today when you were called to walk by faith?',
    'Faith may be weak and still be saving. Where was yours weak today, and did you bring it to Christ anyway?',
    'What promise of God did you stake something on today?',
    'Where did unbelief disguise itself as realism?',
    'You received Christ by faith. Are you living on Him daily, or only remembering you once did?',
    'What would you do differently tomorrow if you truly believed God\'s Word about it?',
    'This Lord\'s Day, where is your faith being tested, and where is it being fed?',
  ],
  // Week 8 — Of Repentance
  [
    'What did you turn from today? What did you turn toward?',
    'Repentance is a grace, not a punishment. Did you receive it as gift or dread it as penalty?',
    'Where did godly grief lead you to change, and where did worldly grief just make you miserable?',
    'Name one specific thing to forsake tomorrow. Will you?',
    'Where did you confess today — to God, and to anyone you wronged?',
    'What sin have you grown comfortable with? Today is the day to be done with it.',
    'This Lord\'s Day, what does full purpose of new obedience look like this week?',
  ],
  // Week 9 — Of the Perseverance of the Saints
  [
    'Two-thirds through. Where have you wanted to quit, and what has kept you?',
    'He who began a good work will finish it. Did you lean on that today, or on yourself?',
    'Where did you persevere today not by gritted teeth but by grace?',
    'What would giving up cost the men watching you?',
    'You cannot finally fall from grace. How does that change how you fight tomorrow?',
    'Where did weariness lie to you today about whether any of this matters?',
    'This Lord\'s Day, thank the Captain who will not lose you. Where have you seen Him keep you?',
  ],
  // Week 10 — Of the Law of God
  [
    'The law is a rule of life, not a way of merit. Did obedience feel like love or like leverage today?',
    'Which commandment did the Spirit press on you today?',
    'Where did you keep the letter and break the spirit?',
    'The law shows the way it cannot give. Where did it expose your need for grace today?',
    'What did loving your neighbor actually require of you today — and did you do it?',
    'Where is your obedience growing quiet and glad rather than loud and anxious?',
    'This Lord\'s Day, where has the law been a lamp this week, not a lash?',
  ],
  // Week 11 — Of Christian Liberty
  [
    'God alone is Lord of the conscience. Where did you bind yourself — or another — beyond His Word today?',
    'You discipline freely, not under compulsion. Did today feel like freedom or like bondage?',
    'Where did liberty tempt you toward license? Where did scruple tempt you toward legalism?',
    'What freedom in Christ did you fail to enjoy today out of fear?',
    'Where did you use your liberty to serve, and where to indulge?',
    'What conscience-matter do you need to settle before God rather than before men?',
    'This Lord\'s Day, for what freedom in Christ are you most grateful?',
  ],
  // Week 12 — Of Religious Worship and the Sabbath
  [
    'Did you worship today, or only perform? What is the difference for you?',
    'Where did private prayer become a duty checked rather than a Father sought?',
    'How did you lead worship in your home today — or did you?',
    'What worldly employment crowded out worship this week?',
    'Where did you treat the means of grace as optional?',
    'What would it look like to prepare your heart for the Lord\'s Day tomorrow?',
    'This Lord\'s Day: corporate worship, family worship, holy rest. Which did you neglect, and why?',
  ],
  // Week 13 — Of Marriage (6 prompts, days 85-90)
  [
    'Your first post is the home. How did you stand it today?',
    'Where did you love your wife as Christ loved the church — in deed, not word only?',
    'What have these 90 days changed in how you lead your household?',
    'Who in your home most needs you to be different tomorrow than you were on Day 1?',
    'What discipline from these weeks will you keep for the rest of your life?',
    'Day 90. Look back over the whole campaign. Where did God meet you? Where will you stand watch next?',
  ],
];

// Flatten prompts into a day->prompt map using the confession_anchors ranges.
const prompts = {};
existing.confession_anchors.forEach((anchor, wi) => {
  const block = promptWeeks[wi] || [];
  for (let d = anchor.day_start; d <= anchor.day_end; d++) {
    prompts[d] = block[d - anchor.day_start] || null;
  }
});

function pick(arr, day) { return arr[(day - 1) % arr.length]; }

// ── Assemble days[] ──
const days = [];
for (let day = 1; day <= 90; day++) {
  const mw = morningWisdomOverrides[day] || morningWisdom(day);
  const entry = {
    day,
    reflection_prompt: prompts[day],
    readings: {
      morning_wisdom: mw,
      husbands_post:  pick(husbandsPost, day),
      fathers_charge: pick(fathersCharge, day),
      citizens_stand: pick(citizensStand, day),
      evening_peace:  eveningPeaceOverrides[day] || pick(eveningPeace, day),
    },
  };
  days.push(entry);
}

// ── Build the final plan object, preserving existing metadata ──
const out = {
  id: existing.id,
  name: existing.name,
  subtitle: existing.subtitle,
  duration_days: existing.duration_days,
  version: 3,
  notes: 'Full 90-day curriculum (v0.6). Five reading tracks, each a curated scripture arc; days 1-7 preserve the original sample week. Reflection prompts are authored in 13 weekly blocks themed to that week\'s LBCF 1689 confession anchor. Generated by scripts/build-watchman-90.js — edit the arrays there and re-run, do not hand-edit this file.',
  completion_message: existing.completion_message,
  streak_grace_per_week: 1,
  graduation: existing.graduation,
  confession_anchors: existing.confession_anchors,
  readings: existing.readings.map(r =>
    r.key === 'citizens_stand' ? { ...r, theme: "Ezekiel \u00b7 Daniel \u00b7 Jeremiah \u00b7 The watchman's charge" } :
    r.key === 'evening_peace'  ? { ...r, theme: 'Psalms \u00b7 Gospels \u00b7 Revelation \u00b7 Rest in Christ' } : r),
  disciplines: existing.disciplines,
  days,
};

fs.writeFileSync(PLAN_PATH, JSON.stringify(out, null, 2) + '\n');

// ── Self-check ──
let blanks = 0, fallbacks = 0;
for (const d of days) {
  if (!d.reflection_prompt) blanks++;
  for (const k of Object.keys(d.readings)) {
    if (!d.readings[k] || !d.readings[k].ref) fallbacks++;
  }
}
console.log('Wrote', PLAN_PATH);
console.log('Days:', days.length, '| blank prompts:', blanks, '| empty reading slots:', fallbacks);
console.log('streak_grace_per_week:', out.streak_grace_per_week);
