#!/usr/bin/env python3
"""
Operation Watchman — 90-Day Plan Generator

Generates content/plans/watchman-90.json from scripture banks + rotation logic.

PLAN SHAPE
----------
Morning Wisdom
  Days 1-30  : Proverbs 1-30 (one chapter per day)
  Day  31    : Proverbs 31 (capstone — the virtuous wife)
  Days 32-90 : NT wisdom cycling through REAL MAN (Reject Passivity, Engage
               Intentionally, Accept Responsibility, Lead Courageously, Manage
               Faithfully, Account Accurately, Never Quit) — 7-day rotation
Husband's Post
  HHAAPPY 7-day rotation, NT-anchored where possible
  (Honest, Honors, Abiding, Adoring, Protecting, Providing, Yields)
Father's Charge
  FULFILLED 9-day rotation, NT-anchored where possible
  (Faithful, Understanding, Loving, Fun, Intentional, Listening, Leading,
   Encouraging, Discipling)
Citizen's Stand
  RESOLUTE 8-day rotation × 3-ring city/state/nation overlay
  2024 acronym: Remembering, Equipped, Serving, Outreaching, Loyal, United,
                Teaching, Engaged
Evening Peace
  Psalms across 90 days. Psalm 119 distributed by stanza.

PERSONALIZATION
---------------
Notes use generic placeholders by default ("your wife", "your son", "your
city", etc.). A separate v0.3 config layer will let each man substitute his
own names. The plan content itself stays universal.

Days 1-7 retain the curated sample-week content from PR #1.

USAGE
-----
  python3 build-watchman-90.py

Writes ./watchman-90.json (sibling of this script).
"""
import json
from pathlib import Path

# ── Framework virtues ────────────────────────────────────────────────────────
REAL_MAN = ["Reject Passivity", "Engage Intentionally", "Accept Responsibility",
            "Lead Courageously", "Manage Faithfully", "Account Accurately",
            "Never Quit"]

HAPPY = ["Honest", "Honors", "Abiding", "Adoring", "Protecting", "Providing",
         "Yields"]

FULFILLED = ["Faithful", "Understanding", "Loving", "Fun", "Intentional",
             "Listening", "Leading", "Encouraging", "Discipling"]

# 2024 handout version — Adam's preferred canonical
RESOLUTE = ["Remembering", "Equipped", "Serving", "Outreaching",
            "Loyal", "United", "Teaching", "Engaged"]

RINGS = ["your city", "your state", "your nation"]


# ── Scripture banks ──────────────────────────────────────────────────────────
# Each virtue maps to a list of (reference, short note) tuples.
# Rotation picks bank[(cycle_index) % len(bank)] so longer banks reduce repeats.

MORNING_NT_BANK = {
    "Reject Passivity": [
        ("Matthew 25:14-30", "Bury the talent or trade with it. Passivity is theft from the Master."),
        ("Ephesians 5:14-17", "Awake, O sleeper. Walk circumspectly. The days are evil."),
        ("James 4:17", "He who knows the right and does it not — to him it is sin."),
        ("Hebrews 6:11-12", "Not sluggish. Imitators of those who through faith inherit the promises."),
        ("Revelation 3:14-22", "Neither hot nor cold. He spits the lukewarm out of His mouth."),
        ("2 Timothy 1:6-7", "Fan into flame the gift of God. Not a spirit of fear, but of power."),
        ("Philippians 3:12-14", "Forgetting what lies behind. Press on toward the goal."),
        ("1 Peter 4:1-2", "Arm yourselves with the same mind. He who suffers in the flesh is done with sin."),
    ],
    "Engage Intentionally": [
        ("Matthew 5:13-16", "Salt that loses its savor is trampled. Light that hides is wasted."),
        ("Colossians 4:5-6", "Walk in wisdom toward outsiders. Speech with grace, seasoned with salt."),
        ("Ephesians 5:15-21", "See then that you walk circumspectly — not as fools, but as wise."),
        ("1 Corinthians 9:24-27", "All run, but one receives the prize. So run that you may obtain."),
        ("James 1:22-25", "Be doers of the word, and not hearers only — deceiving yourselves."),
        ("Romans 12:9-13", "Genuine love. Fervent in spirit. Serving the Lord."),
        ("1 Peter 1:13-16", "Gird up the loins of your mind. Be sober. Set your hope fully."),
        ("Hebrews 10:24-25", "Stir up one another to love and good works. Do not forsake assembling."),
    ],
    "Accept Responsibility": [
        ("Luke 15:11-32", "The prodigal came to himself. The first step home is owning it."),
        ("Matthew 25:31-46", "Sheep or goat. The line is drawn by what you did, not what you said."),
        ("Romans 14:10-12", "Each of us shall give account of himself to God."),
        ("2 Corinthians 5:9-11", "The judgment seat of Christ. The fear of the Lord persuades men."),
        ("Galatians 6:4-5", "Let each man examine his own work. Each shall bear his own load."),
        ("James 5:16", "Confess your faults to one another. The fervent prayer of a righteous man avails."),
        ("1 John 1:5-10", "If we say we have no sin, we deceive ourselves. He is faithful to forgive."),
        ("Luke 12:42-48", "Faithful steward. To whom much is given, much shall be required."),
    ],
    "Lead Courageously": [
        ("Acts 4:13-31", "They marveled at the boldness of unschooled men. They had been with Jesus."),
        ("2 Timothy 1:7", "Not a spirit of fear, but of power, of love, and of a sound mind."),
        ("1 Corinthians 16:13-14", "Watch ye. Stand fast in the faith. Quit you like men. Be strong."),
        ("Hebrews 13:6", "The Lord is my helper. I will not fear what man shall do to me."),
        ("Ephesians 6:10-13", "Be strong in the Lord. Put on the whole armor. Stand."),
        ("Philippians 1:27-30", "Stand fast in one spirit, striving together for the faith."),
        ("Acts 20:24", "I count not my life dear to myself — that I may finish my course with joy."),
        ("2 Timothy 4:1-8", "Preach the word. In season, out of season. I have fought the good fight."),
    ],
    "Manage Faithfully": [
        ("Luke 16:10-13", "He who is faithful in least is faithful in much. You cannot serve two masters."),
        ("1 Corinthians 4:1-2", "Stewards of the mysteries of God. Required of stewards: be found faithful."),
        ("1 Peter 4:10-11", "Each man, as he has received a gift, minister it as a good steward."),
        ("Matthew 6:19-24", "Treasures in heaven. Where your treasure is, your heart will be."),
        ("1 Timothy 6:6-19", "Godliness with contentment is great gain. Rich in good works."),
        ("Luke 14:25-33", "Count the cost before you build. Sit down first and calculate."),
        ("Hebrews 13:5", "Free from the love of money. Be content with what you have."),
        ("1 Timothy 5:8", "He who provides not for his own has denied the faith."),
    ],
    "Account Accurately": [
        ("Hebrews 13:17", "Submit to those who watch for your souls — they shall give account."),
        ("Matthew 12:36-37", "By your words you will be justified — and by your words condemned."),
        ("1 Peter 3:15-16", "Be ready always to give an answer — with meekness and fear."),
        ("James 3:1-12", "Not many should be teachers. We shall receive a stricter judgment."),
        ("2 Corinthians 13:5", "Examine yourselves whether you be in the faith. Prove your own selves."),
        ("1 Corinthians 11:27-31", "Let a man examine himself before he eats. If we judged ourselves, we would not be judged."),
        ("Romans 12:3", "Think of yourself with sober judgment, according to the measure of faith."),
        ("Galatians 6:1-3", "Restore in a spirit of meekness. Consider yourself, lest you also be tempted."),
    ],
    "Never Quit": [
        ("Galatians 6:9", "Be not weary in well-doing. In due season we shall reap, if we faint not."),
        ("2 Timothy 4:7", "I have fought the good fight. I have finished my course. I have kept the faith."),
        ("Hebrews 12:1-3", "Run with patience. Looking unto Jesus, the author and finisher of our faith."),
        ("James 1:2-4", "Count it all joy when you fall into trials. Let patience have her perfect work."),
        ("Romans 5:1-5", "Tribulation works patience. Patience, experience. Experience, hope."),
        ("1 Corinthians 15:58", "Be steadfast, unmovable. Your labor is not in vain in the Lord."),
        ("Philippians 4:13", "I can do all things through Christ who strengthens me."),
        ("Revelation 2:10", "Be faithful unto death. I will give you the crown of life."),
    ],
}

HUSBAND_BANK = {
    "Honest": [
        ("Psalm 139:23-24", "Search me, O God. See if there be any wicked way in me."),
        ("Ephesians 4:25", "Put away lying. Speak truth, each with his neighbor."),
        ("1 John 1:5-10", "If we walk in the light, the blood of Jesus cleanses us from all sin."),
        ("James 5:16", "Confess your faults one to another. Pray for one another, that you may be healed."),
        ("Proverbs 27:5-6", "Open rebuke is better than secret love. Faithful are the wounds of a friend."),
        ("Hebrews 4:12-13", "The Word lays bare. All things are naked before His eyes."),
        ("Matthew 5:37", "Let your yes be yes, your no be no. More than this is from the evil one."),
        ("Galatians 2:11-14", "Paul withstood Peter to the face. He was to be blamed."),
    ],
    "Honors": [
        ("Ephesians 5:25-33", "Husbands, love your wives as Christ loved the church — and gave Himself for her."),
        ("1 Peter 3:7", "Dwell with her with understanding. Give honor — heir together of the grace of life."),
        ("Proverbs 31:28-31", "Her children rise and call her blessed. Her husband also — he praises her."),
        ("Colossians 3:19", "Husbands, love your wives. Be not bitter against them."),
        ("Hebrews 13:4", "Marriage is honorable in all. The bed undefiled."),
        ("1 Corinthians 11:7", "The woman is the glory of the man."),
        ("Genesis 2:18-25", "Bone of my bones, flesh of my flesh. He shall cleave unto his wife."),
        ("Song of Solomon 2:10-13", "Rise up, my love, my fair one, and come away."),
    ],
    "Abiding": [
        ("John 15:1-11", "Abide in Me. The branch cannot bear fruit by itself."),
        ("Psalm 1:1-3", "Blessed is the man... his delight is in the law of the LORD."),
        ("Colossians 3:1-4", "Set your mind on things above. Your life is hid with Christ in God."),
        ("Galatians 2:20", "I have been crucified with Christ. Yet I live; not I, but Christ in me."),
        ("Philippians 4:8-9", "Whatsoever is true, noble, just, pure — think on these things."),
        ("Ephesians 3:14-21", "Rooted and grounded in love. Filled with all the fullness of God."),
        ("1 John 2:6", "He who says he abides in Him ought himself to walk as He walked."),
        ("Romans 8:9-11", "If the Spirit of Him who raised Jesus dwells in you, He shall quicken you."),
    ],
    "Adoring": [
        ("Song of Solomon 4:1-7", "You have ravished my heart, my sister, my spouse."),
        ("Proverbs 5:15-19", "Drink waters out of thine own cistern. Rejoice with the wife of thy youth."),
        ("Song of Solomon 8:6-7", "Set me as a seal upon thine heart. Love is strong as death."),
        ("Proverbs 18:22", "Whoso findeth a wife findeth a good thing — and obtaineth favour of the LORD."),
        ("Genesis 24:67", "Isaac brought her into Sarah's tent. He loved her, and was comforted."),
        ("Ecclesiastes 9:9", "Live joyfully with the wife whom thou lovest, all the days of thy life."),
        ("Song of Solomon 7:10", "I am my beloved's, and his desire is toward me."),
        ("Ephesians 5:28-29", "He that loveth his wife loveth himself. No man ever yet hated his own flesh."),
    ],
    "Protecting": [
        ("1 Peter 3:7", "Husbands, dwell with them according to knowledge. Give honor to the weaker vessel."),
        ("Ephesians 5:25-27", "He gave Himself for her — to sanctify and cleanse her with the washing of water by the word."),
        ("Nehemiah 4:14", "Fight for your brethren, your sons, your daughters, your wives, your houses."),
        ("Psalm 91:1-4", "He shall cover thee with His feathers. His truth shall be thy shield."),
        ("Proverbs 24:11-12", "Deliver those drawn unto death. He that pondereth the heart, considereth it."),
        ("Ephesians 6:10-18", "Put on the whole armor of God. Withstand in the evil day, and having done all, stand."),
        ("Genesis 2:15", "The LORD put him into the garden to dress it and to keep it."),
        ("1 Samuel 30:18-19", "David recovered all. Nothing lacking — small or great, sons or daughters."),
    ],
    "Providing": [
        ("1 Timothy 5:8", "He that provideth not for his own house is worse than an infidel."),
        ("Proverbs 27:23-27", "Be diligent to know the state of thy flocks. Riches are not forever."),
        ("2 Thessalonians 3:10-12", "If any would not work, neither should he eat."),
        ("Proverbs 13:22", "A good man leaveth an inheritance to his children's children."),
        ("Genesis 30:30", "When shall I provide for mine own house also?"),
        ("Proverbs 6:6-11", "Go to the ant, thou sluggard. Consider her ways and be wise."),
        ("Proverbs 22:29", "Seest thou a man diligent in his business? He shall stand before kings."),
        ("Matthew 6:25-34", "Seek first the kingdom of God — and all these things shall be added."),
    ],
    "Yields": [
        ("Philippians 2:3-11", "In lowliness of mind let each esteem other better than themselves."),
        ("Ephesians 5:21", "Submitting yourselves one to another in the fear of God."),
        ("1 Peter 5:5-6", "Be clothed with humility. God resisteth the proud."),
        ("James 4:7-10", "Submit yourselves therefore to God. Humble yourselves in the sight of the Lord."),
        ("Matthew 26:39", "Not as I will, but as Thou wilt."),
        ("Proverbs 19:11", "The discretion of a man defers his anger. It is his glory to overlook a transgression."),
        ("Romans 12:18", "If it be possible, as much as lieth in you, live peaceably with all men."),
        ("Colossians 3:12-14", "Put on bowels of mercies, kindness, humbleness, meekness, longsuffering."),
    ],
}

FATHER_BANK = {
    "Faithful": [
        ("Matthew 25:21", "Well done, good and faithful servant. You were faithful in a few things."),
        ("1 Corinthians 4:2", "It is required in stewards that a man be found faithful."),
        ("Lamentations 3:22-23", "His mercies are new every morning. Great is Thy faithfulness."),
        ("2 Timothy 2:13", "If we are faithless, He remains faithful — He cannot deny Himself."),
        ("Joshua 24:14-15", "As for me and my house, we will serve the LORD."),
        ("Hebrews 10:23", "Hold fast the profession of our faith without wavering."),
        ("Deuteronomy 7:9", "The LORD thy God, the faithful God, keeping covenant to a thousand generations."),
        ("Proverbs 28:20", "A faithful man shall abound with blessings."),
    ],
    "Understanding": [
        ("Psalm 139:13-16", "Thou hast covered me in my mother's womb. Fearfully and wonderfully made."),
        ("Ephesians 6:4", "Provoke not your children to wrath."),
        ("Proverbs 20:5", "Counsel in the heart of man is like deep water. A man of understanding draws it out."),
        ("Proverbs 19:14", "Houses and riches are an inheritance from fathers — but a prudent wife from the LORD."),
        ("Matthew 18:1-6", "Except ye be converted and become as little children, ye shall not enter the kingdom."),
        ("Luke 2:51-52", "Jesus increased in wisdom and stature, and in favor with God and man."),
        ("1 Corinthians 13:11", "When I was a child, I spoke as a child. When I became a man, I put away childish things."),
        ("Proverbs 4:7", "Wisdom is the principal thing. With all thy getting, get understanding."),
    ],
    "Loving": [
        ("1 Corinthians 13:4-7", "Love suffers long, is kind. Beareth all things, hopeth all things, endureth all things."),
        ("1 John 4:7-21", "Beloved, let us love one another — for love is of God."),
        ("John 13:34-35", "A new commandment I give unto you, that ye love one another."),
        ("Romans 12:9-10", "Let love be without dissimulation. Be kindly affectioned with brotherly love."),
        ("1 John 3:16-18", "Let us not love in word, but in deed and in truth."),
        ("Ephesians 4:31-32", "Be ye kind one to another, tenderhearted, forgiving one another."),
        ("Colossians 3:12-14", "Above all these things put on charity, which is the bond of perfectness."),
        ("Ephesians 3:14-19", "That ye may know the love of Christ, which passeth knowledge."),
    ],
    "Fun": [
        ("Proverbs 17:22", "A merry heart doeth good like a medicine. A broken spirit drieth the bones."),
        ("Ecclesiastes 3:1-8", "To every thing there is a season. A time to weep, a time to laugh."),
        ("Ecclesiastes 9:7-10", "Go thy way, eat thy bread with joy. Whatsoever thy hand findeth to do, do it with thy might."),
        ("Psalm 127:3-5", "Children are an heritage of the LORD. Like arrows in the hand of a mighty man."),
        ("Nehemiah 8:10", "The joy of the LORD is your strength."),
        ("Zephaniah 3:17", "He will rejoice over thee with joy. He will joy over thee with singing."),
        ("Luke 15:22-24", "Bring forth the best robe and put it on him. Let us eat and be merry."),
        ("Proverbs 15:13", "A merry heart maketh a cheerful countenance."),
    ],
    "Intentional": [
        ("Deuteronomy 6:6-9", "These words shall be in thine heart. Teach them diligently unto thy children."),
        ("Ephesians 5:15-16", "See then that ye walk circumspectly. Redeeming the time, because the days are evil."),
        ("Proverbs 22:6", "Train up a child in the way he should go. When he is old, he will not depart from it."),
        ("Psalm 78:1-8", "We will not hide them from their children. The next generation might know."),
        ("Joshua 24:15", "Choose you this day whom ye will serve. As for me and my house — the LORD."),
        ("Proverbs 4:1-9", "Hear, ye children, the instruction of a father. Get wisdom; get understanding."),
        ("2 Timothy 3:14-17", "From a child thou hast known the holy Scriptures. Profitable for doctrine, reproof, correction."),
        ("1 Thessalonians 2:11-12", "As a father deals with his own children — exhorting, comforting, charging."),
    ],
    "Listening": [
        ("James 1:19", "Swift to hear, slow to speak, slow to wrath."),
        ("Proverbs 18:13", "He that answereth a matter before he heareth it — it is folly and shame unto him."),
        ("Proverbs 19:20", "Hear counsel and receive instruction, that thou mayest be wise in thy latter end."),
        ("Ecclesiastes 5:1", "Keep thy foot when thou goest to the house of God. Be more ready to hear."),
        ("Hebrews 5:11-14", "Strong meat belongs to them of full age. By use, senses are exercised to discern."),
        ("Matthew 18:15-17", "If thy brother shall trespass against thee, go and tell him his fault — between thee and him alone."),
        ("Proverbs 18:2", "A fool hath no delight in understanding — but in that his heart may discover itself."),
        ("Proverbs 20:5", "The heart of man is like deep water. A man of understanding draweth it out."),
    ],
    "Leading": [
        ("Ephesians 6:4", "Bring them up in the nurture and admonition of the Lord."),
        ("1 Timothy 3:4-5", "One that ruleth well his own house, having his children in subjection."),
        ("Joshua 24:15", "As for me and my house, we will serve the LORD."),
        ("Deuteronomy 6:4-9", "Thou shalt love the LORD thy God with all thine heart. These words shall be in thine heart."),
        ("1 Peter 5:2-4", "Feed the flock of God which is among you. Not by constraint, but willingly."),
        ("Hebrews 13:7", "Remember them which have the rule over you. Follow their faith."),
        ("1 Thessalonians 5:14", "Warn them that are unruly. Comfort the feebleminded. Support the weak. Be patient."),
        ("Proverbs 27:23", "Be thou diligent to know the state of thy flocks. Look well to thy herds."),
    ],
    "Encouraging": [
        ("Hebrews 10:24-25", "Consider one another to provoke unto love and good works."),
        ("1 Thessalonians 5:11", "Comfort yourselves together, and edify one another."),
        ("Ephesians 4:29", "Let no corrupt communication proceed out of your mouth — but that which is good to edify."),
        ("Proverbs 12:25", "Heaviness in the heart maketh it stoop. A good word maketh it glad."),
        ("Hebrews 3:13", "Exhort one another daily, while it is called To day. Lest any be hardened."),
        ("Colossians 3:21", "Fathers, provoke not your children to anger — lest they be discouraged."),
        ("Philippians 4:8", "Whatsoever things are of good report — think on these things."),
        ("Romans 14:19", "Let us therefore follow after the things which make for peace, and edify one another."),
    ],
    "Discipling": [
        ("Deuteronomy 6:6-9", "Teach them diligently to thy children. Talk of them when thou sittest. When thou walkest."),
        ("Matthew 28:18-20", "Go ye therefore, and teach all nations — teaching them to observe all things."),
        ("2 Timothy 2:2", "Commit thou to faithful men, who shall be able to teach others also."),
        ("Proverbs 22:6", "Train up a child in the way he should go. When he is old, he will not depart from it."),
        ("3 John 4", "I have no greater joy than to hear that my children walk in truth."),
        ("Ephesians 6:4", "Bring them up in the nurture and admonition of the Lord."),
        ("Psalm 78:4", "We will not hide them from their children — showing to the generation to come."),
        ("1 Corinthians 11:1", "Be ye followers of me, even as I also am of Christ."),
    ],
}

CITIZEN_BANK = {
    "Remembering": [
        ("Deuteronomy 8:1-18", "Beware lest thou forget the LORD thy God. Thou shalt remember all the way."),
        ("Joshua 4:1-7", "Twelve stones from the Jordan. So your children may ask: What mean these stones?"),
        ("Ecclesiastes 12:1", "Remember now thy Creator in the days of thy youth."),
        ("Psalm 78:5-7", "He commanded our fathers to make them known to their children — that the generation to come might know."),
        ("1 Corinthians 11:23-26", "This do in remembrance of Me. As often as ye eat this bread."),
        ("2 Peter 1:12-15", "I will not be negligent to put you always in remembrance — though ye know and be established."),
        ("Hebrews 13:7", "Remember them which have the rule over you. Whose faith follow."),
        ("Deuteronomy 32:7", "Remember the days of old. Ask thy father, and he will shew thee."),
    ],
    "Equipped": [
        ("Ephesians 6:10-18", "Put on the whole armor of God. Stand against the wiles of the devil."),
        ("2 Timothy 3:16-17", "All Scripture is profitable. That the man of God may be perfect, thoroughly furnished."),
        ("Psalm 144:1", "Blessed be the LORD my strength, which teacheth my hands to war."),
        ("Hebrews 4:12", "The Word of God is quick, and powerful, and sharper than any two-edged sword."),
        ("1 Peter 3:15", "Be ready always to give an answer to every man — with meekness and fear."),
        ("2 Corinthians 10:3-5", "The weapons of our warfare are not carnal — but mighty through God."),
        ("1 Timothy 6:11-12", "Flee these things. Fight the good fight of faith. Lay hold on eternal life."),
        ("Ephesians 4:11-16", "Apostles, prophets, evangelists, pastors, teachers — for the perfecting of the saints."),
    ],
    "Serving": [
        ("Mark 10:42-45", "The Son of man came not to be ministered unto, but to minister."),
        ("Matthew 20:25-28", "Whosoever will be great among you, let him be your minister."),
        ("Galatians 5:13", "By love serve one another."),
        ("1 Peter 4:10", "As every man hath received the gift, even so minister the same one to another."),
        ("Philippians 2:3-8", "Look not every man on his own things — but every man also on the things of others."),
        ("Acts 20:35", "It is more blessed to give than to receive."),
        ("John 13:1-17", "Jesus girded Himself with a towel, and began to wash the disciples' feet."),
        ("Romans 12:9-13", "Distributing to the necessity of saints. Given to hospitality."),
    ],
    "Outreaching": [
        ("Matthew 28:18-20", "Go ye therefore, and teach all nations. Baptizing them, teaching them."),
        ("Acts 1:8", "Ye shall be witnesses unto Me — in Jerusalem, in all Judaea and Samaria, unto the uttermost part of the earth."),
        ("2 Corinthians 5:18-21", "He hath given to us the ministry of reconciliation. We are ambassadors for Christ."),
        ("Romans 10:13-15", "How shall they hear without a preacher? How beautiful are the feet of them that preach the gospel."),
        ("Matthew 5:13-16", "Ye are the salt of the earth. Ye are the light of the world."),
        ("1 Peter 3:15", "Be ready always to give an answer to every man — with meekness and fear."),
        ("Colossians 4:2-6", "Walk in wisdom toward them that are without. Redeeming the time."),
        ("James 5:19-20", "If any of you do err from the truth, and one convert him — he shall save a soul from death."),
    ],
    "Loyal": [
        ("Proverbs 17:17", "A friend loveth at all times. A brother is born for adversity."),
        ("Proverbs 18:24", "A man that hath friends must shew himself friendly. There is a friend that sticketh closer than a brother."),
        ("Proverbs 27:10", "Thine own friend, and thy father's friend, forsake not."),
        ("John 15:13", "Greater love hath no man than this — that a man lay down his life for his friends."),
        ("Ruth 1:16-17", "Whither thou goest, I will go. Thy people shall be my people, and thy God my God."),
        ("2 Samuel 23:13-17", "David's mighty men brake through the host of the Philistines. He poured the water out unto the LORD."),
        ("2 Timothy 4:9-11", "Demas hath forsaken me. Only Luke is with me."),
        ("Hebrews 13:1", "Let brotherly love continue."),
    ],
    "United": [
        ("Ephesians 4:1-6", "One body, one Spirit, one hope, one Lord, one faith, one baptism, one God and Father."),
        ("Psalm 133", "Behold, how good and how pleasant it is for brethren to dwell together in unity."),
        ("1 Corinthians 1:10", "That there be no divisions among you. Perfectly joined together in the same mind."),
        ("John 17:20-23", "That they all may be one. As Thou, Father, art in Me, and I in Thee."),
        ("Philippians 2:1-2", "Be likeminded, having the same love, being of one accord, of one mind."),
        ("Romans 15:5-7", "Be likeminded one toward another, according to Christ Jesus."),
        ("Colossians 3:12-15", "Above all these things put on charity, which is the bond of perfectness."),
        ("Acts 4:32", "The multitude of them that believed were of one heart and of one soul."),
    ],
    "Teaching": [
        ("Matthew 28:18-20", "Teaching them to observe all things whatsoever I have commanded you."),
        ("2 Timothy 2:2", "The same commit thou to faithful men, who shall be able to teach others also."),
        ("Ephesians 4:11-13", "Pastors and teachers — for the perfecting of the saints, for the work of the ministry."),
        ("Titus 2:1-15", "Speak thou the things which become sound doctrine. Aged men, aged women, young men."),
        ("Deuteronomy 6:6-7", "Teach them diligently to thy children. Talk of them when thou sittest. When thou walkest."),
        ("Colossians 3:16", "Let the word of Christ dwell in you richly. Teaching and admonishing one another."),
        ("1 Timothy 4:11-13", "These things command and teach. Give attendance to reading, to exhortation, to doctrine."),
        ("Acts 18:24-28", "Apollos, mighty in the Scriptures. Aquila and Priscilla expounded unto him the way of God more perfectly."),
    ],
    "Engaged": [
        ("Jeremiah 29:7", "Seek the peace of the city whither I have caused you to be carried away. Pray unto the LORD for it."),
        ("Romans 13:1-7", "Let every soul be subject unto the higher powers. The powers that be are ordained of God."),
        ("1 Peter 2:13-17", "Submit yourselves to every ordinance of man for the Lord's sake."),
        ("1 Timothy 2:1-4", "Supplications, prayers, intercessions — for kings, and for all that are in authority."),
        ("Titus 3:1-2", "Put them in mind to be subject to principalities and powers. To be ready to every good work."),
        ("Matthew 5:13-16", "Ye are the light of the world. A city that is set on an hill cannot be hid."),
        ("1 Corinthians 16:13-14", "Watch ye, stand fast in the faith, quit you like men, be strong."),
        ("Philippians 2:14-16", "Do all things without murmurings and disputings. Shine as lights in the world."),
    ],
}

# Psalms for Evening Peace (days 8-90). Days 1-7 already use 1, 23, 46, 91, 103, 121, 139.
# Psalm 119 stanzas distributed periodically. Other Psalms selected for the evening watch.
PSALM_119_STANZAS = [
    ("Psalm 119:1-8 (Aleph)",   "Blessed are the undefiled in the way."),
    ("Psalm 119:9-16 (Beth)",   "Wherewithal shall a young man cleanse his way? By taking heed thereto according to Thy word."),
    ("Psalm 119:17-24 (Gimel)", "Open Thou mine eyes, that I may behold wondrous things out of Thy law."),
    ("Psalm 119:25-32 (Daleth)","My soul cleaveth unto the dust. Quicken Thou me according to Thy word."),
    ("Psalm 119:33-40 (He)",    "Teach me, O LORD, the way of Thy statutes. I shall keep it unto the end."),
    ("Psalm 119:41-48 (Vau)",   "Let Thy mercies come unto me, O LORD. So shall I have wherewith to answer him that reproacheth me."),
    ("Psalm 119:49-56 (Zain)",  "Remember the word unto Thy servant — upon which Thou hast caused me to hope."),
    ("Psalm 119:57-64 (Cheth)", "Thou art my portion, O LORD. I have said that I would keep Thy words."),
    ("Psalm 119:65-72 (Teth)",  "Thou hast dealt well with Thy servant. It is good for me that I have been afflicted."),
    ("Psalm 119:73-80 (Jod)",   "Thy hands have made me and fashioned me. Give me understanding, that I may learn."),
    ("Psalm 119:81-88 (Caph)",  "My soul fainteth for Thy salvation. I hope in Thy word."),
    ("Psalm 119:89-96 (Lamed)", "For ever, O LORD, Thy word is settled in heaven."),
    ("Psalm 119:97-104 (Mem)",  "O how I love Thy law! It is my meditation all the day."),
    ("Psalm 119:105-112 (Nun)", "Thy word is a lamp unto my feet, and a light unto my path."),
    ("Psalm 119:113-120 (Samech)","I hate vain thoughts. But Thy law do I love."),
    ("Psalm 119:121-128 (Ain)", "I have done judgment and justice. Leave me not to mine oppressors."),
    ("Psalm 119:129-136 (Pe)",  "Thy testimonies are wonderful. Therefore doth my soul keep them."),
    ("Psalm 119:137-144 (Tzaddi)","Righteous art Thou, O LORD. Upright are Thy judgments."),
    ("Psalm 119:145-152 (Koph)","I cried with my whole heart. Hear me, O LORD."),
    ("Psalm 119:153-160 (Resh)","Consider mine affliction, and deliver me. For I do not forget Thy law."),
    ("Psalm 119:161-168 (Schin)","Great peace have they which love Thy law. Nothing shall offend them."),
    ("Psalm 119:169-176 (Tau)", "Let my cry come near before Thee, O LORD. Give me understanding according to Thy word."),
]

# Other Psalms selected for evening — order curated by tone (trust, rest, refuge, providence)
EVENING_PSALMS = [
    ("Psalm 4",  "I will both lay me down in peace, and sleep. Thou alone makest me dwell in safety."),
    ("Psalm 16", "I have set the LORD always before me. He is at my right hand. I shall not be moved."),
    ("Psalm 27", "The LORD is my light and my salvation. Whom shall I fear?"),
    ("Psalm 34", "I will bless the LORD at all times. His praise shall continually be in my mouth."),
    ("Psalm 37", "Fret not thyself because of evildoers. Trust in the LORD, and do good."),
    ("Psalm 42", "As the hart panteth after the water brooks, so panteth my soul after Thee, O God."),
    ("Psalm 51", "Create in me a clean heart, O God. Renew a right spirit within me."),
    ("Psalm 62", "My soul, wait thou only upon God. From Him cometh my expectation."),
    ("Psalm 63", "Early will I seek Thee. My soul thirsteth for Thee."),
    ("Psalm 84", "Better is a day in Thy courts than a thousand."),
    ("Psalm 90", "Lord, Thou hast been our dwelling place in all generations. Teach us to number our days."),
    ("Psalm 100","Make a joyful noise unto the LORD, all ye lands."),
    ("Psalm 116","I love the LORD, because He hath heard my voice and my supplications."),
    ("Psalm 118","This is the day which the LORD hath made. We will rejoice and be glad in it."),
    ("Psalm 130","Out of the depths have I cried unto Thee, O LORD."),
    ("Psalm 131","LORD, my heart is not haughty. I have behaved and quieted myself, as a child."),
    ("Psalm 138","Though I walk in the midst of trouble, Thou wilt revive me."),
    ("Psalm 143","Cause me to hear Thy lovingkindness in the morning. For in Thee do I trust."),
    ("Psalm 145","Every day will I bless Thee. I will praise Thy name for ever and ever."),
    ("Psalm 146","Praise the LORD, O my soul. While I live will I praise the LORD."),
    ("Psalm 147","He healeth the broken in heart. He bindeth up their wounds."),
    ("Psalm 148","Let them praise the name of the LORD. His name alone is excellent."),
    ("Psalm 150","Let every thing that hath breath praise the LORD."),
    ("Psalm 8",  "When I consider Thy heavens — what is man, that Thou art mindful of him?"),
    ("Psalm 19", "The heavens declare the glory of God. The law of the LORD is perfect, converting the soul."),
    ("Psalm 30", "Weeping may endure for a night. But joy cometh in the morning."),
    ("Psalm 32", "Blessed is he whose transgression is forgiven. I acknowledged my sin unto Thee."),
    ("Psalm 33", "Sing unto Him a new song. The eye of the LORD is upon them that fear Him."),
    ("Psalm 40", "I waited patiently for the LORD. He inclined unto me, and heard my cry."),
    ("Psalm 56", "What time I am afraid, I will trust in Thee."),
    ("Psalm 61", "From the end of the earth will I cry unto Thee, when my heart is overwhelmed."),
    ("Psalm 65", "Praise waiteth for Thee, O God, in Sion. Thou art the confidence of all the ends of the earth."),
    ("Psalm 67", "God be merciful unto us, and bless us. Cause His face to shine upon us."),
    ("Psalm 71", "In Thee, O LORD, do I put my trust. Forsake me not when my strength faileth."),
    ("Psalm 73", "Nevertheless I am continually with Thee. Thou hast holden me by my right hand."),
    ("Psalm 86", "Bow down Thine ear, O LORD. Hear me, for I am poor and needy."),
    ("Psalm 92", "It is a good thing to give thanks unto the LORD. To shew forth Thy lovingkindness in the morning."),
    ("Psalm 95", "O come, let us worship and bow down. Let us kneel before the LORD our maker."),
    ("Psalm 96", "Sing unto the LORD a new song. Sing unto the LORD, all the earth."),
    ("Psalm 98", "Sing unto the LORD a new song. For He hath done marvellous things."),
    ("Psalm 99", "The LORD reigneth. Let the people tremble. Exalt ye the LORD our God."),
    ("Psalm 101","Mercy and judgment will I sing. I will behave myself wisely in a perfect way."),
    ("Psalm 104","Bless the LORD, O my soul. O LORD my God, Thou art very great."),
    ("Psalm 107","O give thanks unto the LORD, for He is good. His mercy endureth for ever."),
    ("Psalm 113","Praise, O ye servants of the LORD. Praise the name of the LORD."),
    ("Psalm 117","O praise the LORD, all ye nations. Praise Him, all ye people."),
    ("Psalm 120","In my distress I cried unto the LORD. He heard me."),
    ("Psalm 121","I will lift up mine eyes unto the hills. From whence cometh my help."),  # also day 6 — kept distinct
    ("Psalm 122","I was glad when they said unto me, Let us go into the house of the LORD."),
    ("Psalm 123","Unto Thee lift I up mine eyes — O Thou that dwellest in the heavens."),
    ("Psalm 124","If it had not been the LORD who was on our side. Our help is in the name of the LORD."),
    ("Psalm 125","They that trust in the LORD shall be as mount Zion, which cannot be removed."),
    ("Psalm 126","When the LORD turned again the captivity of Zion, we were like them that dream."),
    ("Psalm 127","Except the LORD build the house, they labor in vain that build it."),
    ("Psalm 128","Blessed is every one that feareth the LORD. That walketh in His ways."),
    ("Psalm 134","Bless the LORD, all ye servants of the LORD."),
    ("Psalm 139","O LORD, Thou hast searched me, and known me."),  # also day 7 — extended
    ("Psalm 141","Set a watch, O LORD, before my mouth. Keep the door of my lips."),
    ("Psalm 142","With my voice I cried unto the LORD. I poured out my complaint before Him."),
    ("Psalm 25", "Unto Thee, O LORD, do I lift up my soul. O my God, I trust in Thee."),
    ("Psalm 26", "Examine me, O LORD, and prove me. Try my reins and my heart."),
    ("Psalm 41", "Blessed is he that considereth the poor. The LORD will deliver him in time of trouble."),
]


# ── Reflection prompts pool (assigned by virtue blend) ───────────────────────
REFLECTION_PROMPTS = {
    "Reject Passivity":     "Where did you wait today when God called you to move?",
    "Engage Intentionally": "What did you give your full presence to — and what did you only half-show up for?",
    "Accept Responsibility":"Whose fault did you blame today that was actually yours?",
    "Lead Courageously":    "Where did you fear man more than God today?",
    "Manage Faithfully":    "What did God entrust to you that you spent on yourself?",
    "Account Accurately":   "If today were submitted as a report, what would you redact?",
    "Never Quit":           "What is God asking you to keep doing past the point you wanted to stop?",

    "Honest":   "What did your wife need you to say today that you didn't say?",
    "Honors":   "When she heard you talking about her — to anyone — was she honored?",
    "Abiding":  "Is your marriage running on your spiritual fumes or on Christ's fullness?",
    "Adoring":  "When was the last time you looked at your wife the way you did when you were dating?",
    "Protecting":"What is encroaching on her peace that you've been ignoring?",
    "Providing":"Does she feel covered today — not just paid for?",
    "Yields":   "When she spoke, did you actually change — or did you do what you already planned?",

    "Faithful":     "What did your children see you keep that no one would have known if you'd broken?",
    "Understanding":"What does each of your children need from you that no one else can give them?",
    "Loving":       "Did your children feel loved today, or just managed?",
    "Fun":          "When was the last time your children heard you laugh because they were near?",
    "Intentional":  "Are you discipling your children — or just supervising them?",
    "Listening":    "What did one of your children say today that you almost missed?",
    "Leading":      "Where are you leading your family — and do they know?",
    "Encouraging":  "Whose courage did you build up today, and whose did you tear down?",
    "Discipling":   "If your children imitated only what you did this week — would Christ be honored?",

    "Remembering":  "What has God done for you this year that you have already started to forget?",
    "Equipped":     "Are you formed for the fight, or hoping it doesn't come?",
    "Serving":      "Whom did you serve today that could give you nothing back?",
    "Outreaching":  "Whose name did you carry to God today that does not yet know Him?",
    "Loyal":        "Where did you choose convenience over your post?",
    "United":       "Where did you fracture brothers today — and where did you knit them?",
    "Teaching":     "What truth did you owe someone today that you withheld?",
    "Engaged":      "Where did your city, state, or nation need a Christian presence today — and were you there?",
}


# ── Curated days 1-7 (preserved from PR #1) ──────────────────────────────────
DAYS_1_TO_7 = [
    {
        "day": 1,
        "reflection_prompt": "What post has God assigned you today? What does it mean to stand there?",
        "readings": {
            "morning_wisdom": {"ref": "Proverbs 1", "virtue": "Reject Passivity", "note": "The fear of the LORD is the beginning of knowledge."},
            "husbands_post":  {"ref": "Ephesians 5:22-33", "virtue": "Honest", "note": "Love her as Christ loved the church."},
            "fathers_charge": {"ref": "Deuteronomy 6:1-9", "virtue": "Faithful", "note": "Teach them diligently to your children."},
            "citizens_stand": {"ref": "Romans 12", "virtue": "Remembering", "ring": "your city", "note": "Be not conformed to this world."},
            "evening_peace":  {"ref": "Psalm 1", "note": "Blessed is the man who walks not in the counsel of the wicked."},
        },
    },
    {
        "day": 2,
        "reflection_prompt": "Where did you compromise today? Where did you hold the line?",
        "readings": {
            "morning_wisdom": {"ref": "Proverbs 2", "virtue": "Engage Intentionally", "note": "Seek her as silver, search for her as hidden treasure."},
            "husbands_post":  {"ref": "1 Peter 3:7", "virtue": "Honors", "note": "Live with your wife in an understanding way."},
            "fathers_charge": {"ref": "Deuteronomy 4:9", "virtue": "Understanding", "note": "Keep your soul diligently; make them known to your children."},
            "citizens_stand": {"ref": "Romans 13:1-7", "virtue": "Equipped", "ring": "your state", "note": "Be subject to the governing authorities."},
            "evening_peace":  {"ref": "Psalm 23", "note": "The LORD is my shepherd."},
        },
    },
    {
        "day": 3,
        "reflection_prompt": "What did the fast show you that fullness was hiding?",
        "readings": {
            "morning_wisdom": {"ref": "Proverbs 3", "virtue": "Accept Responsibility", "note": "Trust in the LORD with all your heart."},
            "husbands_post":  {"ref": "Colossians 3:18-19", "virtue": "Abiding", "note": "Husbands, love your wives and do not be harsh with them."},
            "fathers_charge": {"ref": "Psalm 78:1-8", "virtue": "Loving", "note": "Tell the next generation the glorious deeds of the LORD."},
            "citizens_stand": {"ref": "1 Peter 2:13-17", "virtue": "Serving", "ring": "your nation", "note": "Be subject for the Lord's sake to every human institution."},
            "evening_peace":  {"ref": "Psalm 46", "note": "Be still and know that I am God."},
        },
    },
    {
        "day": 4,
        "reflection_prompt": "Who did you fail to love today as Christ loves the church?",
        "readings": {
            "morning_wisdom": {"ref": "Proverbs 4", "virtue": "Lead Courageously", "note": "Keep your heart with all vigilance."},
            "husbands_post":  {"ref": "Proverbs 5:15-20", "virtue": "Adoring", "note": "Drink water from your own cistern."},
            "fathers_charge": {"ref": "Proverbs 22:6", "virtue": "Fun", "note": "Train up a child in the way he should go."},
            "citizens_stand": {"ref": "Daniel 3", "virtue": "Outreaching", "ring": "your city", "note": "Three men who would not bow."},
            "evening_peace":  {"ref": "Psalm 91", "note": "He who dwells in the shelter of the Most High."},
        },
    },
    {
        "day": 5,
        "reflection_prompt": "If your son were watching you this week, what would he learn about being a man?",
        "readings": {
            "morning_wisdom": {"ref": "Proverbs 5", "virtue": "Manage Faithfully", "note": "Rejoice in the wife of your youth."},
            "husbands_post":  {"ref": "Song of Solomon 2", "virtue": "Protecting", "note": "My beloved is mine and I am his."},
            "fathers_charge": {"ref": "Ephesians 6:4", "virtue": "Intentional", "note": "Fathers, do not provoke your children to anger."},
            "citizens_stand": {"ref": "Acts 5:29", "virtue": "Loyal", "ring": "your state", "note": "We must obey God rather than men."},
            "evening_peace":  {"ref": "Psalm 103", "note": "Bless the LORD, O my soul."},
        },
    },
    {
        "day": 6,
        "reflection_prompt": "Where did you fear man more than God today?",
        "readings": {
            "morning_wisdom": {"ref": "Proverbs 6", "virtue": "Account Accurately", "note": "Go to the ant, O sluggard."},
            "husbands_post":  {"ref": "1 Corinthians 13", "virtue": "Providing", "note": "Love is patient, love is kind."},
            "fathers_charge": {"ref": "1 Timothy 3:4-5", "virtue": "Listening", "note": "He must manage his own household well."},
            "citizens_stand": {"ref": "Matthew 5:13-16", "virtue": "United", "ring": "your nation", "note": "You are the salt of the earth."},
            "evening_peace":  {"ref": "Psalm 121", "note": "I lift up my eyes to the hills."},
        },
    },
    {
        "day": 7,
        "reflection_prompt": "What has God done this week that you almost missed?",
        "readings": {
            "morning_wisdom": {"ref": "Proverbs 7", "virtue": "Never Quit", "note": "Keep my commandments and live."},
            "husbands_post":  {"ref": "Genesis 2:18-25", "virtue": "Yields", "note": "It is not good that the man should be alone."},
            "fathers_charge": {"ref": "Joshua 24:15", "virtue": "Leading", "note": "As for me and my house, we will serve the LORD."},
            "citizens_stand": {"ref": "Jeremiah 29:4-7", "virtue": "Teaching", "ring": "your city", "note": "Seek the welfare of the city."},
            "evening_peace":  {"ref": "Psalm 139", "note": "Search me, O God, and know my heart."},
        },
    },
]


# ── Evening Peace assignment for days 8-90 ───────────────────────────────────
# Distribute Psalm 119 stanzas every ~4 days, fill with other Psalms.
def evening_for_day(day):
    """Return (ref, note) for evening peace on this day. Days 1-7 are pre-set."""
    # Position in days 8-90 (0-indexed)
    pos = day - 8
    # Every 4th day gets a Psalm 119 stanza
    if pos % 4 == 0:
        stanza_idx = (pos // 4) % len(PSALM_119_STANZAS)
        return PSALM_119_STANZAS[stanza_idx]
    # Other days: select from EVENING_PSALMS, skipping those covered in days 1-7
    other_idx = (pos - pos // 4) % len(EVENING_PSALMS)
    return EVENING_PSALMS[other_idx]


# ── Morning Wisdom assignment ────────────────────────────────────────────────
def morning_for_day(day):
    """Return (ref, virtue, note) for morning wisdom on this day."""
    rm_idx = (day - 1) % 7
    virtue = REAL_MAN[rm_idx]
    if day <= 30:
        ref = f"Proverbs {day}"
        # Light thematic note tied to the day's REAL MAN virtue (override with chapter-specific)
        notes_by_chapter = {
            1: "The fear of the LORD is the beginning of knowledge.",
            2: "Seek her as silver, search for her as hidden treasure.",
            3: "Trust in the LORD with all your heart.",
            4: "Keep your heart with all vigilance.",
            5: "Rejoice in the wife of your youth.",
            6: "Go to the ant, O sluggard.",
            7: "Keep my commandments and live.",
            8: "Wisdom calls aloud in the street.",
            9: "She has built her house. She has hewn her seven pillars.",
            10: "The mouth of the righteous is a fountain of life.",
            11: "When pride comes, then comes disgrace.",
            12: "He who tills his land will have plenty of bread.",
            13: "He who walks with wise men shall be wise.",
            14: "Every wise woman builds her house.",
            15: "A soft answer turns away wrath.",
            16: "Commit thy works unto the LORD, and thy thoughts shall be established.",
            17: "A merry heart doeth good like a medicine.",
            18: "The tongue has the power of life and death.",
            19: "Better is the poor that walks in his integrity.",
            20: "Wine is a mocker, strong drink is raging.",
            21: "The king's heart is in the hand of the LORD.",
            22: "A good name is rather to be chosen than great riches.",
            23: "When you sit to eat with a ruler, consider diligently what is before you.",
            24: "Be not envious of evil men.",
            25: "It is the glory of God to conceal a thing.",
            26: "Answer not a fool according to his folly, lest thou be like him.",
            27: "Iron sharpens iron. A man sharpens the countenance of his friend.",
            28: "The wicked flee when no man pursues.",
            29: "He who is often reproved, and hardens his neck, shall suddenly be destroyed.",
            30: "Give me neither poverty nor riches. Feed me with food convenient for me.",
        }
        return ref, virtue, notes_by_chapter.get(day, "Wisdom is the principal thing.")
    if day == 31:
        return "Proverbs 31", "Reject Passivity", "Who can find a virtuous woman? Her price is far above rubies."
    # Days 32-90: NT wisdom rotating REAL MAN
    cycle = (day - 32) // 7
    bank = MORNING_NT_BANK[virtue]
    ref, note = bank[cycle % len(bank)]
    return ref, virtue, note


# ── Husband / Father / Citizen assignment ────────────────────────────────────
def husband_for_day(day):
    happy_idx = (day - 1) % 7
    virtue = HAPPY[happy_idx]
    cycle = (day - 1) // 7
    bank = HUSBAND_BANK[virtue]
    ref, note = bank[cycle % len(bank)]
    return ref, virtue, note


def father_for_day(day):
    full_idx = (day - 1) % 9
    virtue = FULFILLED[full_idx]
    cycle = (day - 1) // 9
    bank = FATHER_BANK[virtue]
    ref, note = bank[cycle % len(bank)]
    return ref, virtue, note


def citizen_for_day(day):
    res_idx = (day - 1) % 8
    virtue = RESOLUTE[res_idx]
    ring = RINGS[(day - 1) % 3]
    cycle = (day - 1) // 8
    bank = CITIZEN_BANK[virtue]
    ref, note = bank[cycle % len(bank)]
    return ref, virtue, ring, note


# ── Build full plan ──────────────────────────────────────────────────────────
def build_day(day):
    if day <= 7:
        return DAYS_1_TO_7[day - 1]

    m_ref, m_virtue, m_note = morning_for_day(day)
    h_ref, h_virtue, h_note = husband_for_day(day)
    f_ref, f_virtue, f_note = father_for_day(day)
    c_ref, c_virtue, c_ring, c_note = citizen_for_day(day)
    e_ref, e_note = evening_for_day(day)

    # Reflection prompt — alternate between the 4 framework virtues
    # Day mod 4 picks which framework's virtue prompt to surface
    prompt_picks = [m_virtue, h_virtue, f_virtue, c_virtue]
    prompt_virtue = prompt_picks[(day - 1) % 4]
    reflection = REFLECTION_PROMPTS.get(prompt_virtue, "Stand your post.")

    # Day 90 closing note
    if day == 90:
        reflection = "Ninety days. You held the post. What did the LORD form in you that He could not have formed any other way?"

    return {
        "day": day,
        "reflection_prompt": reflection,
        "readings": {
            "morning_wisdom": {"ref": m_ref, "virtue": m_virtue, "note": m_note},
            "husbands_post":  {"ref": h_ref, "virtue": h_virtue, "note": h_note},
            "fathers_charge": {"ref": f_ref, "virtue": f_virtue, "note": f_note},
            "citizens_stand": {"ref": c_ref, "virtue": c_virtue, "ring": c_ring, "note": c_note},
            "evening_peace":  {"ref": e_ref, "note": e_note},
        },
    }


def build_plan():
    plan = {
        "id": "watchman-90",
        "name": "Operation Watchman",
        "subtitle": "90-Day Men's Formation",
        "duration_days": 90,
        "version": 2,
        "scripture_focus": "New Testament (Matthew → Revelation) with Proverbs 1-31 anchoring the first month and Psalms running the evening watch through all 90 days.",
        "notes": "v2 curriculum. Each watch rotates through a named acronym framework (REAL MAN / HHAAPPY / FULFILLED / RESOLUTE). Notes use generic phrasing — a future personalization layer will substitute the user's wife, children, city, state, and nation.",
        "readings": [
            {"key": "morning_wisdom", "title": "Morning Wisdom", "theme": "Proverbs · Psalms · Wisdom literature"},
            {"key": "husbands_post",  "title": "Husband's Post", "theme": "Ephesians · Marriage & love passages"},
            {"key": "fathers_charge", "title": "Father's Charge", "theme": "Deuteronomy · Legacy & instruction"},
            {"key": "citizens_stand", "title": "Citizen's Stand", "theme": "Romans · Civic duty & righteousness"},
            {"key": "evening_peace",  "title": "Evening Peace",   "theme": "Reflection · Gratitude · Rest"},
        ],
        "disciplines": [
            {"key": "cold_shower",    "title": "Cold Shower",          "theme": "Discipline the body, strengthen the mind"},
            {"key": "fasting",        "title": "Fasting",              "theme": "Skip a meal · Fast from distraction"},
            {"key": "no_alcohol",     "title": "No Alcohol",           "theme": "Clear mind · Full presence"},
            {"key": "no_screens",     "title": "No Screens After 9PM", "theme": "Protect sleep · Protect your mind"},
            {"key": "prayer_morning", "title": "Morning Prayer",       "theme": "Before the battle begins"},
            {"key": "prayer_evening", "title": "Evening Prayer",       "theme": "Account · Surrender · Rest"},
        ],
        "frameworks": {
            "morning_wisdom": {
                "acronym": "REAL MAN",
                "cadence": "7-day rotation (day-of-week)",
                "virtues": REAL_MAN,
            },
            "husbands_post": {
                "acronym": "HHAAPPY",
                "cadence": "7-day rotation (day-of-week)",
                "virtues": HAPPY,
            },
            "fathers_charge": {
                "acronym": "FULFILLED",
                "cadence": "9-day rotation",
                "virtues": FULFILLED,
            },
            "citizens_stand": {
                "acronym": "RESOLUTE",
                "cadence": "8-day virtue rotation × 3-ring (city/state/nation) overlay",
                "virtues": RESOLUTE,
                "rings": RINGS,
            },
        },
        "days": [build_day(d) for d in range(1, 91)],
    }
    return plan


def main():
    plan = build_plan()
    out = Path(__file__).parent / "watchman-90.json"
    out.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {out} ({len(plan['days'])} days)")


if __name__ == "__main__":
    main()
