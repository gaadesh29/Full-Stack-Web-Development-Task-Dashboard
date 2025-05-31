import Head from 'next/head';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Dashboard</title>
      </Head>
      <main className="p-6 text-white">
        <h1 className="text-3xl font-bold">Welcome to the Dashboard</h1>
      </main>
    </div>
  );
}