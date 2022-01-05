CREATE TABLE IF NOT EXISTS guild_stats
(
    guildid bigint NOT NULL,
    year smallint NOT NULL DEFAULT 0,
    no_goodbye_fanette smallint DEFAULT 0,
    CONSTRAINT guild_stats_pkey PRIMARY KEY (guildid, year)
);

CREATE TABLE IF NOT EXISTS users
(
    userid bigint NOT NULL,
    birthday date,
    CONSTRAINT users_pkey PRIMARY KEY (userid)
);

CREATE TABLE IF NOT EXISTS users_stats
(
    userid bigint NOT NULL,
    year smallint NOT NULL DEFAULT 0,
    message_sent integer DEFAULT 0,
    voice_channel_time bigint DEFAULT 0,
    music_played integer DEFAULT 0,
    feur integer DEFAULT 0,
    CONSTRAINT users_stats_pkey PRIMARY KEY (userid, year),
    CONSTRAINT fk_userid FOREIGN KEY (userid)
        REFERENCES public.users (userid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users_mentions
(
    userid bigint NOT NULL,
    mentioned_user bigint NOT NULL,
    year smallint NOT NULL DEFAULT 0,
    number_of_mentions integer DEFAULT 0,
    CONSTRAINT users_mentions_pkey PRIMARY KEY (userid, mentioned_user, year),
    CONSTRAINT fk_year FOREIGN KEY (userid, year)
        REFERENCES public.users_stats (userid, year) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);
