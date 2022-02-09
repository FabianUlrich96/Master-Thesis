create table API(
    name varchar(200) not null,
    token varchar(50) not null,
    service varchar(50) not null,
    primary key (name)
);

create table Job(
    id int not null AUTO_INCREMENT,
    api varchar(200) not null,
    name varchar(200) not null,
    date date not null,
    query VARCHAR(200) not null,
    done boolean not null default false,
    failed boolean not null default false,
    state double not null default 0.0,
    primary key (id),
    foreign key (api) references API (name) on delete cascade
);

create table Video_List(
    video_id varchar(100),
	kind varchar(100),
    job int not null,
    page int not null,
    date date not null,
    primary key (video_id),
    foreign key (job) references Job (id) on delete cascade
);

create table Comment_List(
    video_id varchar(100),
    comment text,
    primary key (video_id),
    foreign key (video_id) references Video_List(video_id) on delete cascade
);