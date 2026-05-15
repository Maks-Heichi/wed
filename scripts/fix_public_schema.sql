-- Query Tool на базе postgres:
ALTER DATABASE mydatabase OWNER TO mydatabaseuser;

-- Query Tool на базе mydatabase:
ALTER SCHEMA public OWNER TO mydatabaseuser;

GRANT USAGE, CREATE ON SCHEMA public TO mydatabaseuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mydatabaseuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mydatabaseuser;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT ALL ON TABLES TO mydatabaseuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT ALL ON SEQUENCES TO mydatabaseuser;
