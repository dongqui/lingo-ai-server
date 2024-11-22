// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.

// Setup type definitions for built-in Supabase Runtime APIs
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

import OpenAI from "npm:openai";

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

    const { title, userId, content } = await req.json();

    const imageUrls = await openai.images.generate({
      model: "dall-e-3",
      prompt:
        `A children's illustrated diary page with a cute, simple drawing style, as if drawn by a child. The title is ${title} and the content is ${content}`,
      n: 1,
      size: "1024x1024",
      quality: "standard",
      style: "natural",
    });

    const imageResponse = await fetch(imageUrls.data[0].url!);

    const { data, error } = await supabaseClient.storage
      .from("vivid")
      .upload(
        `${userId}/${Date.now()}.png`,
        await imageResponse.arrayBuffer(),
        {
          contentType: "image/png",
          upsert: false,
        },
      );

    if (error) throw error;

    const { data: { publicUrl } } = supabaseClient.storage.from("vivid")
      .getPublicUrl(
        data.path,
      );

    return new Response(JSON.stringify({ imageUrl: publicUrl }), {
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
