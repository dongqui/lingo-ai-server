// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.

// Setup type definitions for built-in Supabase Runtime APIs
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

import OpenAI from "npm:openai";
import Sharp from "npm:@img/sharp-linux-x64";
import { createClient, SupabaseClient } from "npm:@supabase/supabase-js";

const supabaseClient: SupabaseClient = createClient(
  Deno.env.get("V_SUPABASE_URL")!,
  Deno.env.get("V_SUPABASE_SERVICE_ROLE_KEY")!,
);

Deno.serve(async (req) => {
  try {
    const openai = new OpenAI({
      apiKey: Deno.env.get("OPENAI_API_KEY"),
    });

    const { content } = await req.json();

    if (!content) {
      throw new Error("Content is required");
    }

    const imageUrls = await openai.images.generate({
      model: "dall-e-3",
      prompt: content +
        ", cute simple drawing style, pastel colors, children's book illustration",
      n: 1,
      size: "1024x1024",
      quality: "standard",
      style: "natural",
    });

    const imageUrl = imageUrls.data[0].url!;
    const imageResponse = await fetch(imageUrl);
    const imageBuffer = await imageResponse.arrayBuffer();

    const resizedImageBuffer = await Sharp(imageBuffer)
      .resize(512, 512)
      .toBuffer();

    const { data, error } = await supabaseClient.storage
      .from("diary-images")
      .upload(`${Date.now()}.png`, resizedImageBuffer, {
        contentType: "image/png",
        upsert: false,
      });
    console.log(data);
    if (error) throw error;

    return new Response(JSON.stringify({ imageUrl: imageUrls.data[0].url }), {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  } catch (error) {
    console.log(error);
    return new Response(
      JSON.stringify({ error: (error as Error)?.message || error }),
      {
        headers: { "Content-Type": "application/json" },
        status: 500,
      },
    );
  }
});

/* To invoke locally:

  1. Run `supabase start` (see: https://supabase.com/docs/reference/cli/supabase-start)
  2. Make an HTTP request:

  curl -i --location --request POST 'http://127.0.0.1:54321/functions/v1/generate-diary-image' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \
    --header 'Content-Type: application/json' \
    --data '{"name":"Functions"}'

*/
