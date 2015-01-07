/* sbc_version.css - Tags the DB with the instance information */

% if instance != 'prod':
#site-slogan:after {
    content: "=== ${instance_desc.upper()} INSTANCE ===";
}
#site-slogan {
    border: 1px solid ${instance_color};
}
% endif